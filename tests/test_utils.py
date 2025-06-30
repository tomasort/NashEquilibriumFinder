"""
Tests for utility functions
"""
import pytest

from nash_equilibrium.utils import (
    from_list_to_beliefs,
    get_coordinates_string,
    print_section_header,
    print_subsection_header,
)


class TestFromListToBeliefs:
    """Test from_list_to_beliefs function"""

    def test_simple_beliefs(self):
        """Test formatting simple belief vectors"""
        result = from_list_to_beliefs([0.5, 0.5])
        assert result == "(0.500, 0.500)"

    def test_single_element(self):
        """Test single element belief vector"""
        result = from_list_to_beliefs([1.0])
        assert result == "(1.000)"

    def test_three_elements(self):
        """Test three element belief vector"""
        result = from_list_to_beliefs([0.333, 0.333, 0.334])
        assert result == "(0.333, 0.333, 0.334)"

    def test_precision_formatting(self):
        """Test that formatting uses 3 decimal places"""
        result = from_list_to_beliefs([1.0 / 3, 2.0 / 3])
        assert "0.333" in result
        assert "0.667" in result

    def test_empty_list(self):
        """Test empty list"""
        result = from_list_to_beliefs([])
        assert result == "()"

    def test_zero_probabilities(self):
        """Test with zero probabilities"""
        result = from_list_to_beliefs([1.0, 0.0, 0.0])
        assert result == "(1.000, 0.000, 0.000)"


class TestGetCoordinatesString:
    """Test get_coordinates_string function"""

    def test_empty_coordinates(self):
        """Test empty coordinates list"""
        result = get_coordinates_string([])
        assert result == "None"

    def test_single_coordinate(self):
        """Test single coordinate"""
        result = get_coordinates_string([(0, 1)])
        assert "A2" in result and "B1" in result

    def test_multiple_coordinates(self):
        """Test multiple coordinates"""
        result = get_coordinates_string([(0, 0), (1, 1)])
        assert "A1" in result and "B1" in result
        assert "A2" in result and "B2" in result

    def test_coordinate_indexing(self):
        """Test that coordinates are converted to 1-indexed display"""
        # Input is (row, col) 0-indexed, output should be (A_col+1, B_row+1)
        result = get_coordinates_string([(1, 0)])
        assert "(A1, B2)" in result

    def test_multiple_coordinates_formatting(self):
        """Test formatting of multiple coordinates"""
        result = get_coordinates_string([(0, 0), (1, 1), (2, 2)])
        # Should have proper spacing between coordinates
        assert "   " in result  # Multiple spaces between coordinates


class TestPrintHeaders:
    """Test header printing functions"""

    def test_print_section_header_success(self):
        """Test successful section header printing"""
        # These functions print to stdout, we just test they don't crash
        try:
            print_section_header("Test Section")
            # If we get here, it didn't crash
            assert True
        except Exception:
            pytest.fail("print_section_header raised an exception")

    def test_print_section_header_empty(self):
        """Test section header with empty string"""
        try:
            print_section_header("")
            assert True
        except Exception:
            pytest.fail("print_section_header raised an exception with empty string")

    def test_print_subsection_header_success(self):
        """Test successful subsection header printing"""
        try:
            print_subsection_header("Test Subsection")
            assert True
        except Exception:
            pytest.fail("print_subsection_header raised an exception")

    def test_print_subsection_header_empty(self):
        """Test subsection header with empty string"""
        try:
            print_subsection_header("")
            assert True
        except Exception:
            pytest.fail("print_subsection_header raised an exception with empty string")

    def test_print_headers_with_special_characters(self):
        """Test headers with special characters"""
        try:
            print_section_header("Test with émojis 🎮 and symbols @#$%")
            print_subsection_header("Test with émojis 🎮 and symbols @#$%")
            assert True
        except Exception:
            pytest.fail("Header functions failed with special characters")


class TestUtilityFunctionEdgeCases:
    """Test edge cases and error conditions for utility functions"""

    def test_from_list_to_beliefs_with_none(self):
        """Test from_list_to_beliefs with invalid input"""
        result = from_list_to_beliefs(None)
        assert result == "()"  # The function treats None as falsy, returns empty tuple format

    def test_get_coordinates_string_with_none(self):
        """Test get_coordinates_string with None input"""
        result = get_coordinates_string(None)
        assert result == "None"

    def test_large_numbers_formatting(self):
        """Test formatting with large numbers"""
        result = from_list_to_beliefs([1000.123456, 2000.987654])
        assert "1000.123" in result
        assert "2000.988" in result

    def test_very_small_numbers_formatting(self):
        """Test formatting with very small numbers"""
        result = from_list_to_beliefs([0.0001, 0.9999])
        assert "0.000" in result
        assert "1.000" in result

    def test_coordinates_boundary_values(self):
        """Test coordinates with boundary values"""
        # Test with large indices
        result = get_coordinates_string([(9, 9)])
        assert "A10" in result and "B10" in result

        # Test with zero indices
        result = get_coordinates_string([(0, 0)])
        assert "A1" in result and "B1" in result
