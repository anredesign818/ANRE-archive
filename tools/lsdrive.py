# usage: python3 lsdrive.py <folder_id> <out.json>  — recursive listing of a public Drive folder (no download)
import sys, json, requests
import importlib; df=importlib.import_module("gdown.download_folder")
sess=requests.Session()
root=df._download_and_parse_google_drive_link(sess=sess, folder_id=sys.argv[1], quiet=True, verify=True, timeout=60)
out=[]
def walk(f,path):
    for c in f.children:
        p=f"{path}/{c.name}" if path else c.name
        if c.is_folder(): walk(c,p)
        else: out.append({'id':c.id,'path':p,'type':c.type})
walk(root,'')
json.dump({'root':root.name,'files':out},open(sys.argv[2],'w'),ensure_ascii=False)
print(root.name,len(out))
