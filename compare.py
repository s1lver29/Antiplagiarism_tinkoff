import argparse
import ast
import re


def create_parser() -> argparse.Namespace:
    pattern = re.compile(r".+\.txt")

    parser = argparse.ArgumentParser(
        description="Checking two files for anti-plagiarism"
    )

    parser.add_argument(
        "indir_files", type=str, help="Input directory for text file to compare"
    )
    parser.add_argument(
        "outdir_scores",
        type=str,
        help="Directory for output text file with comparison score",
    )

    args = parser.parse_args()
    for f in args._get_kwargs():
        if pattern.match(f[1]) is None:
            raise ValueError("Error name {} {}".format(f[0], f[1]))

    return args


class antiplagiarism:
    def __init__(self):
        self.scores = []

    def get_file_text_code(self, f: str) -> str:
        """
        Reading the source file

        Parameters
        ----------
        f: str
            Filename *.py

        """
        pattern_py = re.compile(r".+\.py")

        if pattern_py.match(f) is None:
            raise ValueError(
                "Incorrect file {}. Need file with *.py extension".format(f)
            )

        with open(f, "r") as sourse:
            text = ast.dump(ast.parse(sourse.read()))

        text = text.strip()

        return text

    # TODO: Как-то токенизировать весь исходный код для проверки кода "внутреннего", без импортов библиотек
    def preprocessing_code(self, code: str) -> str:
        pass

    def levenshtein(self, code_1: str, code_2: str) -> int:
        """
        Проверка двух тестов кода на схожесть (Алгоритм Вагнера — Фишера)

        Parameters
        ----------
        code_1 : str
            First original text
        code_2 : str
            Second source text

        Returns
        ----------
        curr_row[n] : int
            Levenshtein distance
        """

        n, m = sorted([len(code_1), len(code_2)])
        code_1, code_2 = sorted([code_1, code_2], key=len)

        curr_row = range(n + 1)
        for i in range(1, m + 1):
            prev_row, curr_row = curr_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = (
                    prev_row[j] + 1,
                    curr_row[j - 1] + 1,
                    prev_row[j - 1],
                )
                if code_1[j - 1] != code_2[i - 1]:
                    change += 1
                curr_row[j] = min(add, delete, change)

        return curr_row[n]

    # Проверка двух текстов кода на схожесть
    def similarity(self, filenames: list) -> float:
        """
        Проверка на схожесть двух исходников и запись метрики в файл

        Parameters
        ----------
        filenames: list[str]
            Source file names

        Return
        ----------
        None
        """

        if len(filenames) != 2:
            raise ValueError(
                "Number of files for one comparison 2. Input {}".format(len(filenames))
            )

        code_1 = self.get_file_text_code(filenames[0])
        code_2 = self.get_file_text_code(filenames[1])

        dist = self.levenshtein(code_1, code_2)

        score = 1 - (dist / min(len(code_1), len(code_2)))

        return score

    # Чтение текстового файла и вывод сходство файлов
    def plagiatism(self, text_file: str, output_file: str) -> None:
        """
        Чтение текстового файла для сравнения двух исходников *.py

        Parameters
        ----------
        text_file : str
            Source text file
        output_file : str
            Output file with file similarity score

        Returns
        ----------
        None
        """

        with open(text_file, "r") as ft:
            for line in ft:
                filenames = line.strip().split()
                self.scores.append(self.similarity(filenames))

        with open(output_file, "w") as fo:
            for score in self.scores:
                fo.write(str(round(score, 2)) + "\n")


if __name__ == "__main__":
    try:
        args = create_parser()
        antiplagiarism().plagiatism(
            text_file=args.indir_files, output_file=args.outdir_scores
        )
    except ValueError:
        raise
