from django.test import TestCase
from rest_framework.test import APIRequestFactory
from api.councils import CouncilViewSet


class CouncilsTest(TestCase):
    fixtures = ["polling_stations/apps/api/fixtures/test_councils.json"]

    def setUp(self):
        factory = APIRequestFactory()
        self.request = factory.get("/foo", format="json")

    def test_list(self):
        response = CouncilViewSet.as_view({"get": "list"})(self.request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))

    def test_valid_council(self):
        response = CouncilViewSet.as_view({"get": "retrieve"})(
            self.request, pk="X01000001"
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual("X01000001", response.data["council_id"])

    def test_bad_council(self):
        response = CouncilViewSet.as_view({"get": "retrieve"})(self.request, pk="FOO")
        # should return 404 if council does not exist
        self.assertEqual(404, response.status_code)

    def test_geo(self):
        geo_response = CouncilViewSet.as_view({"get": "geo"})(
            self.request, pk="X01000001"
        )
        response = CouncilViewSet.as_view({"get": "retrieve"})(
            self.request, pk="X01000001"
        )

        # geo_response should contain geometry
        self.assertEqual(True, ("geometry" in geo_response.data))
        self.assertEqual("MultiPolygon", geo_response.data["geometry"]["type"])

        # (non-geo) response should not contain geometry
        self.assertEqual(True, ("geometry" not in response.data))

        self.assertEqual(response.data["name"], geo_response.data["properties"]["name"])

    def test_null_area(self):
        response = CouncilViewSet.as_view({"get": "geo"})(self.request, pk="X01000002")
        self.assertEqual(None, response.data["geometry"])
