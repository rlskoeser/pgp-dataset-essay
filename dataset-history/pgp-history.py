import io
import csv
from datetime import datetime

from git import Repo

repo = Repo(".")

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
            reader = csv.DictReader(fp)
            # for now, we just want to count number of documents
            num_records = len([row for row in reader])
            outcsv.writerow([commit_day, 'documents', num_records])

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
            reader = csv.DictReader(fp)

            # count total number of fragments AND fragments with images
            frag_total = 0
            frag_img_total = 0
            for row in reader:
                frag_total += 1
                if row.get('iiif_url'):
                    frag_img_total += 1
            outcsv.writerow([commit_day, 'fragments', frag_total])
            outcsv.writerow([commit_day, 'fragment_images', frag_img_total])

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
            reader = csv.DictReader(fp)

            # count total number of fragments AND fragments with images
            transcription_total = 0
            translation_total = 0
            for row in reader:
                doc_relation =row.get('doc_relation')
                if doc_relation == "Digital Edition":
                    transcription_total += 1
                if doc_relation == "Digital Translation":
                    translation_total += 1

            outcsv.writerow([commit_day, 'transcriptions', transcription_total])
            outcsv.writerow([commit_day, 'translations', translation_total])


