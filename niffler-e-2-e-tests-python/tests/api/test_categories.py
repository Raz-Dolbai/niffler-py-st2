from clients.spends_client import SpendsHttpClient


def test_add_category(spends_client: SpendsHttpClient):
    model = spends_client.add_category("carbox")
    print(model)

