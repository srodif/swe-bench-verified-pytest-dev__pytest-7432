"""Test to reproduce the skip location reporting issue with --runxfail"""

def test_skip_location_reporting_with_runxfail(testdir):
    """Test that skip location is correctly reported even when --runxfail is used"""
    p = testdir.makepyfile(
        """
        import pytest
        @pytest.mark.skip
        def test_skip_location():
            assert 0
        """
    )
    
    # Test without --runxfail (this should work correctly)
    result = testdir.runpytest(p, "-rs")
    result.stdout.fnmatch_lines([
        "*SKIPPED*test_skip_location.py:3: unconditional skip*"
    ])
    
    # Test with --runxfail (this currently breaks but should work the same)
    result = testdir.runpytest(p, "-rs", "--runxfail")
    # This should show the test location, not the internal pytest location
    result.stdout.fnmatch_lines([
        "*SKIPPED*test_skip_location.py:3: unconditional skip*"
    ])
    # It should NOT show the internal skipping.py location
    assert "skipping.py" not in result.stdout.str()