"""
BLOOD COMPATIBILITY AI ENGINE
==============================
A rule-based expert system for determining medically compatible donor blood groups.

This module implements standard blood type compatibility rules used in medical transfusions.
The AI determines which donor blood groups can safely provide blood for a requested blood group.

Author: Blood Bank Application
Date: 2026
"""

# Blood Compatibility Rules (Based on Medical Standards)
# Key: Requested Blood Group -> List of Compatible Donor Blood Groups
BLOOD_COMPATIBILITY_RULES = {
    "O+": ["O+", "O-"],           # O+ can receive from O+ and O-
    "O-": ["O-"],                  # O- (Universal Donor) can only give to O-
    "A+": ["A+", "A-", "O+", "O-"],  # A+ can receive from A+, A-, O+, O-
    "A-": ["A-", "O-"],            # A- can receive from A-, O-
    "B+": ["B+", "B-", "O+", "O-"],  # B+ can receive from B+, B-, O+, O-
    "B-": ["B-", "O-"],            # B- can receive from B-, O-
    "AB+": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"],  # AB+ (Universal Recipient)
    "AB-": ["A-", "B-", "O-", "AB-"]  # AB- can receive from A-, B-, O-, AB-
}


def get_compatible_blood_groups(requested_blood_group):
    """
    Determine compatible donor blood groups for a requested blood group.
    
    Args:
        requested_blood_group (str): The blood group needed (e.g., 'A+', 'B-', 'AB+')
    
    Returns:
        list: A list of compatible donor blood groups, or empty list if invalid input
    
    Example:
        >>> get_compatible_blood_groups('A+')
        ['A+', 'A-', 'O+', 'O-']
    """
    requested_blood_group = str(requested_blood_group).strip().upper()
    
    # Validate input
    if requested_blood_group not in BLOOD_COMPATIBILITY_RULES:
        return []
    
    compatible_donors = BLOOD_COMPATIBILITY_RULES[requested_blood_group]
    return compatible_donors


def filter_compatible_donors(requested_blood_group, available_donors):
    """
    Filter a list of donors to only include those with compatible blood groups.
    
    Args:
        requested_blood_group (str): The blood group needed
        available_donors (list): List of donor dictionaries with 'blood_group' key
    
    Returns:
        list: Filtered list of compatible donors
    
    Example:
        >>> donors = [
        ...     {'email': 'donor1@test.com', 'blood_group': 'A+'},
        ...     {'email': 'donor2@test.com', 'blood_group': 'AB+'},
        ...     {'email': 'donor3@test.com', 'blood_group': 'B+'}
        ... ]
        >>> filter_compatible_donors('A+', donors)
        # Returns only donor1 and donor3 with compatible blood groups
    """
    compatible_blood_groups = get_compatible_blood_groups(requested_blood_group)
    
    if not compatible_blood_groups:
        return []
    
    filtered_donors = [
        donor for donor in available_donors
        if donor.get('blood_group', '').strip().upper() in compatible_blood_groups
    ]
    
    return filtered_donors


def is_compatible(donor_blood_group, requested_blood_group):
    """
    Check if a specific donor blood group is compatible with the requested blood group.
    
    Args:
        donor_blood_group (str): The donor's blood group
        requested_blood_group (str): The requested blood group
    
    Returns:
        bool: True if compatible, False otherwise
    
    Example:
        >>> is_compatible('O+', 'A+')
        True
        >>> is_compatible('B+', 'A+')
        False
    """
    compatible_blood_groups = get_compatible_blood_groups(requested_blood_group)
    donor_blood_group = str(donor_blood_group).strip().upper()
    
    return donor_blood_group in compatible_blood_groups


def get_all_valid_blood_groups():
    """
    Get a list of all valid blood groups in the system.
    
    Returns:
        list: All valid blood group types
    """
    return list(BLOOD_COMPATIBILITY_RULES.keys())


def explain_compatibility(requested_blood_group):
    """
    Generate a human-readable explanation of blood group compatibility.
    
    Args:
        requested_blood_group (str): The blood group to explain
    
    Returns:
        str: A formatted explanation string
    """
    compatible = get_compatible_blood_groups(requested_blood_group)
    
    if not compatible:
        return f"Invalid blood group: {requested_blood_group}"
    
    compatible_str = ", ".join(compatible)
    return f"Blood Group {requested_blood_group} can receive from: {compatible_str}"


# AI Engine Statistics and Analytics
def get_compatibility_statistics():
    """
    Generate statistics about blood group compatibility in the system.
    
    Returns:
        dict: Statistics including universal donors, universal recipients, etc.
    """
    stats = {
        "universal_donor": "O-",
        "universal_recipient": "AB+",
        "total_blood_groups": len(BLOOD_COMPATIBILITY_RULES),
        "compatibility_rules": len(BLOOD_COMPATIBILITY_RULES)
    }
    return stats


if __name__ == "__main__":
    # Test the AI Engine
    print("=" * 60)
    print("BLOOD COMPATIBILITY AI ENGINE - TEST SUITE")
    print("=" * 60)
    
    # Test 1: Get compatible blood groups
    print("\n[TEST 1] Compatible Blood Groups for A+:")
    print(f"Result: {get_compatible_blood_groups('A+')}")
    
    # Test 2: Check specific compatibility
    print("\n[TEST 2] Is O+ compatible with A+?")
    print(f"Result: {is_compatible('O+', 'A+')}")
    
    # Test 3: Filter donors
    print("\n[TEST 3] Filter compatible donors:")
    test_donors = [
        {'email': 'donor1@test.com', 'name': 'John', 'blood_group': 'O+'},
        {'email': 'donor2@test.com', 'name': 'Jane', 'blood_group': 'B+'},
        {'email': 'donor3@test.com', 'name': 'Bob', 'blood_group': 'A+'}
    ]
    compatible = filter_compatible_donors('A+', test_donors)
    for donor in compatible:
        print(f"  - {donor['name']} ({donor['blood_group']})")
    
    # Test 4: Explain compatibility
    print("\n[TEST 4] Compatibility Explanation:")
    print(explain_compatibility('AB+'))
    
    # Test 5: All valid blood groups
    print("\n[TEST 5] All Valid Blood Groups:")
    print(get_all_valid_blood_groups())
    
    print("\n" + "=" * 60)
