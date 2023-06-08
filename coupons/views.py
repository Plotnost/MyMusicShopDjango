from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import PercentageCoupon, FixedPriceCoupon
from .forms import CouponApplyForm


def search_coupons(request, coupon_ids):
    if 'percentage_coupon_id' in request.session:
        current_percentage_coupon_id = request.session['percentage_coupon_id']
        if current_percentage_coupon_id in coupon_ids:
            coupon_ids.remove(current_percentage_coupon_id)
            request.session['coupon_ids'] = coupon_ids
    if 'fixed_coupon_ids' in request.session:
        fixed_coupon_ids = request.session['fixed_coupon_ids']
        for fixed_coupon_id in fixed_coupon_ids:
            if fixed_coupon_id in coupon_ids:
                coupon_ids.remove(fixed_coupon_id)
        request.session['coupon_ids'] = coupon_ids


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    coupon_ids = request.session.get('coupon_ids', [])
    if form.is_valid():
        code = form.cleaned_data['code']

        try:

            percentage_coupon = PercentageCoupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now,
                                                             active=True)
            current_percentage_coupon_id = request.session.get('percentage_coupon_id')
            if current_percentage_coupon_id:
                current_percentage_coupon = PercentageCoupon.objects.get(id=current_percentage_coupon_id)
                if percentage_coupon.discount > current_percentage_coupon.discount:
                    request.session['percentage_coupon_id'] = percentage_coupon.id
            else:
                request.session['percentage_coupon_id'] = percentage_coupon.id

            if percentage_coupon.id not in coupon_ids:
                coupon_ids.append(percentage_coupon.id)
                request.session['coupon_ids'] = coupon_ids

        except PercentageCoupon.DoesNotExist:
            search_coupons(request, coupon_ids)

        try:
            fixed_coupon = FixedPriceCoupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now,
                                                        active=True)
            fixed_coupon_ids = request.session.get('fixed_coupon_ids', [])
            if fixed_coupon.id not in fixed_coupon_ids:
                fixed_coupon_ids.append(fixed_coupon.id)
                request.session['fixed_coupon_ids'] = fixed_coupon_ids

            if fixed_coupon.id not in coupon_ids:
                coupon_ids.append(fixed_coupon.id)
                request.session['coupon_ids'] = coupon_ids

        except FixedPriceCoupon.DoesNotExist:
            search_coupons(request, coupon_ids)

    return redirect('cart:cart_detail')


def clear_coupons(request):
    request.session.pop('percentage_coupon_id', None)
    request.session.pop('fixed_coupon_ids', None)
    request.session.pop('coupon_ids', None)
    return redirect('cart:cart_detail')
