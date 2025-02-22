import pytest
from ui import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Purchase Product' in response.data

def test_submit_purchase(client):
    response = client.post('/submit_purchase', data={
        'purchase_option': 'purchase',
        'search_product': 'Example Product',
        'add_to_cart': '2',
        'order_product': 'Order Example Product'
    })
    assert response.status_code == 200
    assert b'Form submitted successfully!' in response.data