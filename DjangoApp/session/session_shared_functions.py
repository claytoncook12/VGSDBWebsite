def check_youtube_url(url: str):
    """
    Checks on youtube embed url for conditions.
    
    Parameters
    ----------
      url (str): url string
    
    Returns
    -------
      bool: if url valid
      str: error message 
    """

    start_with = "https://www.youtube.com/embed/"
    if not url.startswith(start_with):
        return False, f'Url must start with {start_with}'

    split_url = url.split("/")
    if split_url[4] == "":
        return False, f'Url must have characters after "{start_with}"'
    
    return True, None

if __name__ == "__main__":
    # Test Conditions For Functions
    print(check_youtube_url("asdasd")) # False
    print(check_youtube_url("https://www.youtube.com/embed/")) # False
    print(check_youtube_url("https://www.youtube.com/embed/xw20aM2rw4o")) # True