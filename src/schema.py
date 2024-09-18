class SQL:
    """SQL Queries for the database"""
    create_albums_table = """
    CREATE TABLE IF NOT EXISTS albums (
        website TEXT,
        year INTEGER,
        rank INTEGER,
        title TEXT,
        PRIMARY KEY (website, year, rank)
    )
    """

    create_spotify_table = """
    CREATE TABLE IF NOT EXISTS spotify (
        spotify_id TEXT,
        artist TEXT,
        album TEXT,
        PRIMARY KEY (spotify_id)
    )"""
    create_text_to_spotify_table = """
    CREATE TABLE IF NOT EXISTS text_to_spotify (
        artist TEXT,
        album TEXT,
        spotify_id TEXT,
        PRIMARY KEY (artist,album)
    )
    """



    insert_album = """
    INSERT OR REPLACE INTO albums (website, year, rank, title)
    VALUES (?, ?, ?, ?)
    """
    get_album = """
    SELECT * FROM albums WHERE website = ? AND year = ? AND rank = ?
    """
    get_all_albums = """
    SELECT * FROM albums
    """
