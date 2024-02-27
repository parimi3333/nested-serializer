from rest_framework import serializers
from .models import invoice, invoicedetails

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = invoicedetails
        fields = ["description","quantity","unit_price","price"]

class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailSerializer(many=True)

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        Invoice = invoice.objects.create(**validated_data)
        for detail_data in details_data:
            invoicedetails.objects.create(Invoice=Invoice, **detail_data)
        return Invoice

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        instance.date = validated_data.get('date', instance.date)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.save()
        for detail_data in details_data:
            detail_id = detail_data.get('id')
            if detail_id:
                detail = instance.details.filter(id=detail_id).first()
                if detail:
                    detail.description = detail_data.get('description', detail.description)
                    detail.quantity = detail_data.get('quantity', detail.quantity)
                    detail.unit_price = detail_data.get('unit_price', detail.unit_price)
                    detail.price = detail_data.get('price', detail.price)
                    detail.save()
                else:
                    invoicedetails.objects.update(Invoice=instance, **detail_data)
            else:
                invoicedetails.objects.update(Invoice=instance, **detail_data)

        return instance
    class Meta:
        model = invoice
        fields = ['id', 'date', 'customer_name', 'details']
