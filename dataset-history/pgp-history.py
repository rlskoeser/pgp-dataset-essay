import io
import csv
from datetime import datetime

import polars as pl

from git import Repo

repo = Repo("../pgp-metadata")

with open("pgp-dataset-history.csv", "w", encoding="utf-8-sig") as output:
    outcsv = csv.writer(output)
    outcsv.writerow(['date', 'type', 'count'])

    # for documents - get total 
    last_day = None
    print("## documents")
    for c in repo.iter_commits(paths="data/documents.csv"):
        commit_date = datetime.fromtimestamp(c.committed_date)
        # get just the day for comparing and reporting
        commit_day = commit_date.date()
        # just get data for one commit per day
        if commit_day == last_day:
            continue
        last_day = commit_day

        data_file = c.tree / "data/documents.csv"
        with io.BytesIO(data_file.data_stream.read()) as f:
            fp = io.StringIO(f.read().decode("utf-8-sig"))
            doc_df = pl.read_csv(fp)
            # for now, we just want to count number of documents
            outcsv.writerow([commit_day, 'documents', doc_df.height])

    # for fragments - get total / total with images
    print("## fragments")    
    last_day = None
    for c in repo.iter_commits(paths="data/fragments.csv"):
        commit_date = datetime.fromtimestamp(c.committed_date)
        # get just the day for comparing and reporting
        commit_day = commit_date.date()
        # just get data for one commit per day
        if commit_day == last_day:
            continue
        last_day = commit_day

        data_file = c.tree / "data/fragments.csv"
        with io.BytesIO(data_file.data_stream.read()) as f:
            fp = io.StringIO(f.read().decode("utf-8-sig"))
            # earlier exports had a duplicate problem; ignore that and count unique
            frag_df = pl.read_csv(fp).unique()

            # record total number of fragments AND fragments with images
            outcsv.writerow([commit_day, 'fragments', frag_df.height])
            outcsv.writerow([commit_day, 'fragment_images', 
                frag_df.filter(pl.col("iiif_url").is_not_null()).height])

    # for footnotes - get # of digital editions, digital translations
    print("## transcriptions / translations")        
    last_day = None
    for c in repo.iter_commits(paths="data/footnotes.csv"):
        commit_date = datetime.fromtimestamp(c.committed_date)
        # get just the day for comparing and reporting
        commit_day = commit_date.date()
        # just get data for one commit per day
        if commit_day == last_day:
            continue
        last_day = commit_day

        data_file = c.tree / "data/footnotes.csv"
        with io.BytesIO(data_file.data_stream.read()) as f:
            fp = io.StringIO(f.read().decode("utf-8-sig"))
            foonotes_df = pl.read_csv(fp)

            # count digital editions & digital translations
            outcsv.writerow([commit_day, 'transcriptions', 
                foonotes_df.filter(pl.col("doc_relation").eq("Digital Edition")).height])
            outcsv.writerow([commit_day, 'translations', 
                foonotes_df.filter(pl.col("doc_relation").eq("Digital Translation")).height])


    # people
    print("## people")    
    last_day = None
    for c in repo.iter_commits(paths="data/people.csv"):
        commit_date = datetime.fromtimestamp(c.committed_date)
        # get just the day for comparing and reporting
        commit_day = commit_date.date()
        # just get data for one commit per day
        if commit_day == last_day:
            continue
        last_day = commit_day

        data_file = c.tree / "data/people.csv"
        with io.BytesIO(data_file.data_stream.read()) as f:
            fp = io.StringIO(f.read().decode("utf-8-sig"))
            # ignore parsing errors (can't infer date range); we just want a count
            people_df = pl.read_csv(fp, ignore_errors=True)

            outcsv.writerow([commit_day, 'people', people_df.height])


    # places
    print("## places")    
    last_day = None
    for c in repo.iter_commits(paths="data/places.csv"):
        commit_date = datetime.fromtimestamp(c.committed_date)
        # get just the day for comparing and reporting
        commit_day = commit_date.date()
        # just get data for one commit per day
        if commit_day == last_day:
            continue
        last_day = commit_day

        data_file = c.tree / "data/places.csv"
        with io.BytesIO(data_file.data_stream.read()) as f:
            fp = io.StringIO(f.read().decode("utf-8-sig"))
            places_df = pl.read_csv(fp)

            outcsv.writerow([commit_day, 'places', places_df.height])