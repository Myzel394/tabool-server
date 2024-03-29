from apps.django.main.homework.mixins.tests import HomeworkTestMixin

__all__ = [
    "HomeworkAutocompleteTest"
]


class HomeworkAutocompleteTest(HomeworkTestMixin):
    TEST_TYPES = [
        "Vortrag", "Hausaufgabe", "Präsentation", "Nachhilfe", "Rede", "Unterricht", "Nachmittag"
    ]

    def setUp(self) -> None:
        self.user = self.Login_student()
        self.__class__.associated_student = self.user

        for element in self.TEST_TYPES:
            self.Create_homework(
                type=element
            )

    @staticmethod
    def flat_text(result: list[dict]) -> list[str]:
        return [
            element["text"]
            for element in result
        ]

    def test_autocompletes_exact_match(self):
        response = self.client.get("/api/autocomplete/homework/type/", {
            "q": "Vortrag"
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        self.assertIn("Vortrag", self.flat_text(response.data["results"]))

    def test_autocomplete_part_of_whole(self):
        response = self.client.get("/api/autocomplete/homework/type/", {
            "q": "Hausauf"
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        self.assertIn("Hausaufgabe", self.flat_text(response.data["results"]))

    def test_random(self):
        response = self.client.get("/api/autocomplete/homework/type/", {
            "q": "Nach"
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
