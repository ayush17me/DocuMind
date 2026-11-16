"""Live paired evaluation with synthetic facts and deterministic answer checks."""
import json
from core import build,chat_model,run,REFUSAL

pages = [("Archive","The archive opens at 08:45."),("Locker","The locker code is 7129."),
         ("Shuttle","The shuttle departs from Birch Gate."),("Cafe","The cafe closes at noon."),
         ("Library","Library loans last fourteen days."),("Lab","The lab is on floor six.")]
cases = [("When does the archive open?","Archive","08:45"),("What is the locker code?","Locker","7129"),
         ("Where does the shuttle depart from?","Shuttle","birch gate"),("Who manages the cafe?",None,REFUSAL)]
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    index,model = build(pages),chat_model()
    for question,source,expected in cases:
        for verify in (False,True):
            answer,t = run(index,model,question,verify=verify)
            print(json.dumps(dict(question=question,checker=verify,answer=answer,
                hit_at_4=(source+".0" in t["sources"]) if source else None,
                reference_match=expected.lower() in answer.lower(),trace=t)))
