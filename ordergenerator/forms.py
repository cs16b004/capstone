from django import forms

class OrderForm(forms.Form):
    TYPE_CHOICES  = [("LM", "Limit"),("MR","Market"),]
    CAT_CHOICES   = [("Buy","Buy"), ("Sell","Sell")]
    EXTRA_CHOICES = [("Yes","Yes"),("No","No")]
    ALL_CHOICES   = [("Yes","Yes"),("No","No")]
    order_category     = forms.CharField(required=True, max_length=10, widget=forms.Select(choices=CAT_CHOICES))
    order_quantity     = forms.IntegerField(required=True)
    order_type         = forms.CharField(required=True, widget=forms.Select(choices= TYPE_CHOICES))
    order_price        = forms.FloatField(required=True)
    extra              = forms.CharField(required=True, widget=forms.Select(choices= EXTRA_CHOICES))
    All_or_none        = forms.BooleanField(required=False)
    Minimum_fill       = forms.IntegerField(required=False)
    Disclosed_Quantity = forms.IntegerField(required=False)
    All_or_none        = forms.CharField(required=False, widget = forms.Select(choices = ALL_CHOICES))
    