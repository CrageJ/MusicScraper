class SQL:
    """SQL Queries for the database"""

    # Stores scraped data
    create_albums_table = """
    CREATE TABLE IF NOT EXISTS albums (
        website TEXT,
        year INTEGER,
        rank INTEGER,
        album TEXT,
        artist TEXT,
        PRIMARY KEY (website, year, rank)
    )
    """

    # Stores data from spotify
    create_spotify_table = """
    CREATE TABLE IF NOT EXISTS spotify (
        spotify_id TEXT,
        album TEXT,
        artist TEXT,
        genres TEXT,
        release_date TEXT,
        image_url TEXT,
        PRIMARY KEY (spotify_id)
    )"""

    # Pairs the album/text combination to the spotify id
    create_text_to_spotify_table = """
    CREATE TABLE IF NOT EXISTS text_to_spotify (
        album TEXT,
        artist TEXT,
        spotify_id TEXT,
        PRIMARY KEY (artist,album)
    )
    """

    insert_album = """
    INSERT OR REPLACE INTO albums (website, year, rank, album, artist)
    VALUES (?, ?, ?, ?, ?)
    """

    insert_spotify = """
    INSERT OR REPLACE INTO spotify (spotify_id, album, artist, genres, release_date, image_url)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    insert_text_to_spotify = """
    INSERT OR REPLACE INTO text_to_spotify (album, artist, spotify_id)
    VALUES (?, ?, ?)
    """

    get_spotify = """
    SELECT DISTINCT * FROM spotify WHERE album = ? AND artist = ?
    """

    # this creates the display table for scraped content
    get_albums_range_top_x = """
    SELECT
        a.website,
        a.year,
        a.rank,
        a.album,
        a.artist,
        s.genres,
        s.release_date,
        s.image_url
    FROM
        albums a
    LEFT JOIN
        text_to_spotify ts ON a.album = ts.album AND a.artist = ts.artist
    LEFT JOIN
        spotify s ON ts.spotify_id = s.spotify_id
    WHERE
        a.year >= ? AND a.year <= ? AND a.rank <= ?
    ORDER BY
        a.website, a.year, a.rank"""

    get_albums_aggregated = """
    SELECT DISTINCT
        a.album,
        a.artist,
        COUNT(a.website) AS website_count,
        AVG(a.rank) AS average_rank,
        MIN(a.year) AS year,
        s.genres,
        s.release_date,
        s.image_url
    FROM
        albums a
    LEFT JOIN
        text_to_spotify ts ON a.album = ts.album AND a.artist = ts.artist
    LEFT JOIN
        spotify s ON ts.spotify_id = s.spotify_id
    WHERE
        a.year >= ? AND a.year <= ?
    GROUP BY
        a.album, a.artist
    ORDER BY
        average_rank ASC, website_count DESC
"""
