from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Customer
# Create your views here.
def home(request):
    return render(request, 'index.html')


from io import BytesIO
def render_pdf_view(request):
    customer = Customer.objects.first()
    context = {'customer': customer, 'image': customer.logo.path}

    template = get_template('PDFs/pdf_download.html')
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
    # print(customer.__dict__)
    # Create a Django response object, and specify content_type as pdf
    # response = HttpResponse(content_type='application/pdf')
    # if download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # elif display:
    # response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.


    # create a pdf
    # pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    # if pisa_status.err:
    #    return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response