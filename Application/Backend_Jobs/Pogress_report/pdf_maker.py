from jinja2 import Template
from weasyprint import HTML
import uuid

def format_report(template, data,lists,cards,name,email):
  with open(template) as f:
    html = Template(f.read())
    html = html.render(data=data,lists=lists,cards=cards,name=name,email=email)
    return html


def create_pdf(data,lists,cards,name,email):
  try:
    message = format_report("./templates/report_template.html",data=data,lists=lists,cards=cards,name=name,email=email)
    html = HTML(string=message)
    file_name = "report_"+str(name)+"_"+str(uuid.uuid4())+".pdf"
    html.write_pdf(target=file_name)
    response = {"file_name":file_name,"message":message}
    return response
  except Exception as e:
    return -1