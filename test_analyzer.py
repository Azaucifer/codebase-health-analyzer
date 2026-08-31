from analyzer import get_health_rating

def test_get_health_rating():
    assert get_health_rating(100) == "Excellent"
    assert get_health_rating(90) == "Excellent"
    assert get_health_rating(89) == "Good"
    assert get_health_rating(75) == "Good"
    assert get_health_rating(74) == "Needs Improvement"
    assert get_health_rating(50) == "Needs Improvement"
    assert get_health_rating(49) == "Poor"
    assert get_health_rating(0) == "Poor"