"""Helper functions for rank role management."""

def format_rank(rank_name: str) -> str:
    """Format a rank name for display."""
    # Slice and capitalize: e.g., "SP1dan" becomes "SP 1 Dan"
    if len(rank_name) < 3:
        return rank_name  # Return as is if too short to format
    
    # if chuuden or kaiden, formatting is a little different. e.g. "spchuuden" becomes "SP Chuuden"
    if rank_name.endswith("chuuden") or rank_name.endswith("kaiden"):
        prefix = rank_name[:2]  # e.g., "sp" or "dp"
        suffix = rank_name[2:]  # e.g., "chuuden" or "kaiden"
        return f"{prefix.upper()} {suffix.capitalize()}"

    prefix = rank_name[:2]  # e.g., "sp" or "dp"
    number = rank_name[2:-3]  # e.g., "1" or "10"
    suffix = rank_name[-3:]  # e.g., "dan" or "kyu"
    return f"{prefix.upper()} {number} {suffix.capitalize()}"

def get_rank_congrats_message(user_mention: str, rank_name: str) -> str:
    """Return a congratulatory message for a user attaining a rank."""
    if "7kyu" in rank_name:
        return f"{user_mention} has begun a journey! Congratulations on achieving {format_rank(rank_name)}!"
    elif "1dan" in rank_name:
        return f"{user_mention} has reached the first of many dans! Congratulations on achieving {format_rank(rank_name)}!"
    elif "sp7dan" in rank_name:
        return f"{user_mention} HAS BESTED THE SAFARI AND ATTAINED {format_rank(rank_name)}!"
    elif "10dan" in rank_name:
        return f"Everything until now was a warm-up. {user_mention} has reached {format_rank(rank_name)}. Good luck on the coming challenges!"
    elif "chuuden" in rank_name:
        return f"{user_mention} has one last rung to climb! Congratulations on achieving {format_rank(rank_name)}!"
    elif "kaiden" in rank_name:
        return f"After a long journey, {user_mention} has climbed to the summit! Congratulations on achieving {format_rank(rank_name)}!"
    else:
        return f"{user_mention} has achieved {format_rank(rank_name)}! Congratulations!"