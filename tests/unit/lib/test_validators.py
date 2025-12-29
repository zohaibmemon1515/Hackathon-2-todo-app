"""
Unit tests for validator utilities
"""
from src.lib.validators import (
    validate_task_title,
    validate_task_description,
    validate_task_completed,
    validate_task_id
)


def test_validate_task_title_with_valid_string():
    """Test that valid task titles return True"""
    assert validate_task_title("Valid Title") is True
    assert validate_task_title("A") is True
    assert validate_task_title("Title with spaces") is True


def test_validate_task_title_with_empty_string():
    """Test that empty task titles return False"""
    assert validate_task_title("") is False


def test_validate_task_title_with_whitespace_only():
    """Test that whitespace-only task titles return False"""
    assert validate_task_title("   ") is False
    assert validate_task_title("\t\n") is False


def test_validate_task_title_with_non_string():
    """Test that non-string inputs return False"""
    assert validate_task_title(None) is False
    assert validate_task_title(123) is False
    assert validate_task_title([]) is False
    assert validate_task_title({}) is False


def test_validate_task_description_with_valid_string():
    """Test that valid task descriptions return True"""
    assert validate_task_description("Valid Description") is True
    assert validate_task_description("") is True
    assert validate_task_description("A") is True
    assert validate_task_description("Description with spaces") is True
    assert validate_task_description(None) is True  # Description is optional


def test_validate_task_description_with_non_string():
    """Test that non-string descriptions return False (except None)"""
    assert validate_task_description(123) is False
    assert validate_task_description([]) is False
    assert validate_task_description({}) is False


def test_validate_task_completed_with_valid_boolean():
    """Test that valid boolean values return True"""
    assert validate_task_completed(True) is True
    assert validate_task_completed(False) is True


def test_validate_task_completed_with_non_boolean():
    """Test that non-boolean values return False"""
    assert validate_task_completed(1) is False
    assert validate_task_completed(0) is False
    assert validate_task_completed("True") is False
    assert validate_task_completed("False") is False
    assert validate_task_completed(None) is False
    assert validate_task_completed([]) is False


def test_validate_task_id_with_valid_positive_integer():
    """Test that valid positive integers return True"""
    assert validate_task_id(1) is True
    assert validate_task_id(100) is True
    assert validate_task_id(999999) is True


def test_validate_task_id_with_zero_or_negative():
    """Test that zero or negative integers return False"""
    assert validate_task_id(0) is False
    assert validate_task_id(-1) is False
    assert validate_task_id(-100) is False


def test_validate_task_id_with_non_integer():
    """Test that non-integer values return False"""
    assert validate_task_id("1") is False
    assert validate_task_id(1.5) is False
    assert validate_task_id(True) is False
    assert validate_task_id(None) is False
    assert validate_task_id([]) is False