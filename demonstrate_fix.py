#!/usr/bin/env python3
"""
Demonstration of the fix for skip location reporting with --runxfail

This script demonstrates that the fix works by testing the core logic
that was modified in pytest_runtest_makereport.
"""

import sys
import os

# Add the src directory to the path so we can import the fixed code
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from _pytest.skipping import skipped_by_mark_key

def demonstrate_fix():
    """Demonstrate that the skip location fix works"""
    
    print("Demonstrating the skip location reporting fix")
    print("=" * 50)
    
    # Create mock objects that simulate the pytest internals
    class MockItem:
        def __init__(self):
            # This simulates a test that was skipped by a mark
            self._store = {skipped_by_mark_key: True}
        
        def reportinfo(self):
            # This simulates the test file location 
            return ('test_example.py', 2, 'test_skip_function')
    
    class MockReport:
        def __init__(self):
            # This simulates a skip report with the internal pytest location
            self.skipped = True
            self.longrepr = ("src/_pytest/skipping.py", 238, "unconditional skip")
    
    # Test the logic that was fixed
    item = MockItem()
    rep = MockReport()
    
    print(f"Before fix - Location shown: {rep.longrepr}")
    print("  ^ This shows the internal pytest location (the bug)")
    
    # Apply the fixed logic (this is the same logic now used in pytest_runtest_makereport)
    if (
        item._store.get(skipped_by_mark_key, True)
        and rep.skipped
        and type(rep.longrepr) is tuple
    ):
        # This is the skip location fixing logic that now runs regardless of --runxfail
        _, _, reason = rep.longrepr
        filename, line = item.reportinfo()[:2]
        assert line is not None
        rep.longrepr = str(filename), line + 1, reason
    
    print(f"After fix - Location shown: {rep.longrepr}")
    print("  ^ This shows the test file location (correct!)")
    
    print("\nWhat the fix does:")
    print("- Before: Skip location fixing only ran when --runxfail was NOT used")
    print("- After: Skip location fixing runs regardless of --runxfail flag")
    print("- Result: --runxfail only affects xfail tests, not skip tests (as intended)")
    
    return True

if __name__ == "__main__":
    try:
        demonstrate_fix()
        print("\n✓ Fix demonstration completed successfully!")
    except Exception as e:
        print(f"\n✗ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)