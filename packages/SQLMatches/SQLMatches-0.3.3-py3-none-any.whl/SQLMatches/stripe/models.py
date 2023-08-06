# -*- coding: utf-8 -*-

"""
GNU General Public License v3.0 (GPL v3)
Copyright (c) 2020-2021 WardPearce
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


from typing import Dict, List, Any


class RecurringModel:
    aggregate_usage: None
    interval: str
    interval_count: int
    usage_type: str
    metadata: Dict[str, Any]

    def __init__(self, aggregate_usage: None, interval: str,
                 interval_count: int, usage_type: str,
                 metadata: Dict[str, Any]) -> None:
        self.aggregate_usage = aggregate_usage
        self.interval = interval
        self.interval_count = interval_count
        self.usage_type = usage_type
        self.metadata = metadata


class PriceModel:
    id: str
    object: str
    active: bool
    billing_scheme: str
    created: int
    currency: str
    livemode: bool
    lookup_key: None
    nickname: None
    product: str
    recurring: RecurringModel
    tiers_mode: None
    transform_quantity: None
    type: str
    unit_amount: int
    unit_amount_decimal: int
    metadata: Dict[str, Any]

    def __init__(self, id: str, object: str, active: bool, billing_scheme: str,
                 created: int, currency: str, livemode: bool, lookup_key: None,
                 nickname: None, product: str,
                 recurring: Dict[str, Any], tiers_mode: None,
                 transform_quantity: None, type: str, unit_amount: int,
                 unit_amount_decimal: int, metadata: Dict[str, Any]) -> None:
        self.id = id
        self.object = object
        self.active = active
        self.billing_scheme = billing_scheme
        self.created = created
        self.currency = currency
        self.livemode = livemode
        self.lookup_key = lookup_key
        self.nickname = nickname
        self.product = product
        self.recurring = RecurringModel(**recurring)
        self.tiers_mode = tiers_mode
        self.transform_quantity = transform_quantity
        self.type = type
        self.unit_amount = unit_amount
        self.unit_amount_decimal = unit_amount_decimal
        self.metadata = metadata


class DatumModel:
    id: str
    object: str
    billing_thresholds: None
    created: int
    price: PriceModel
    quantity: int
    subscription: str
    tax_rates: List[Any]
    metadata: Dict[str, Any]

    def __init__(self, id: str, object: str, billing_thresholds: None,
                 created: int, price: Dict[str, Any],
                 quantity: int, subscription: str,
                 tax_rates: List[Any], metadata: Dict[str, Any]) -> None:
        self.id = id
        self.object = object
        self.billing_thresholds = billing_thresholds
        self.created = created
        self.price = PriceModel(**price)
        self.quantity = quantity
        self.subscription = subscription
        self.tax_rates = tax_rates
        self.metadata = metadata


class ItemsModel:
    object: str
    data: List[DatumModel]
    has_more: bool
    url: str
    metadata: Dict[str, Any]

    def __init__(self, object: str, data: List[Dict[str, Any]], has_more: bool,
                 url: str, metadata: Dict[str, Any]) -> None:
        self.object = object
        self.data = [DatumModel(**datum) for datum in data]
        self.has_more = has_more
        self.url = url
        self.metadata = metadata


class InvoiceSettingsModel:
    custom_fields: None
    default_payment_method: None
    footer: None
    metadata: Dict[str, Any]

    def __init__(self, custom_fields: str, default_payment_method: str,
                 footer: str, metadata: Dict[str, Any]) -> None:
        self.custom_fields = custom_fields
        self.default_payment_method = default_payment_method
        self.footer = footer
        self.metadata = metadata


class CustomerModel:
    id: str
    object: str
    address: str
    balance: int
    created: int
    currency: str
    default_source: str
    delinquent: bool
    description: str
    discount: float
    email: str
    invoice_prefix: str
    invoice_settings: InvoiceSettingsModel
    livemode: bool
    name: str
    next_invoice_sequence: int
    phone: str
    preferred_locales: List[Any]
    shipping: str
    tax_exempt: str
    metadata: Dict[str, Any]

    def __init__(self, id: str, object: str, address: str, balance: int,
                 created: int, currency: str, default_source: str,
                 delinquent: bool, description: str, discount: float,
                 email: str, invoice_prefix: str,
                 invoice_settings: InvoiceSettingsModel, livemode: bool,
                 name: str, next_invoice_sequence: int, phone: str,
                 preferred_locales: List[Any], shipping: str,
                 tax_exempt: str, metadata: Dict[str, Any]) -> None:
        self.id = id
        self.object = object
        self.address = address
        self.balance = balance
        self.created = created
        self.currency = currency
        self.default_source = default_source
        self.delinquent = delinquent
        self.description = description
        self.discount = discount
        self.email = email
        self.invoice_prefix = invoice_prefix
        self.invoice_settings = invoice_settings
        self.livemode = livemode
        self.name = name
        self.next_invoice_sequence = next_invoice_sequence
        self.phone = phone
        self.preferred_locales = preferred_locales
        self.shipping = shipping
        self.tax_exempt = tax_exempt
        self.metadata = metadata


class CardModel:
    id: str
    object: str
    address_city: str
    address_country: str
    address_line1: str
    address_line1_check: str
    address_line2: str
    address_state: str
    address_zip: int
    address_zip_check: str
    brand: str
    country: str
    customer: str
    cvc_check: str
    dynamic_last4: str
    exp_month: int
    exp_year: int
    fingerprint: str
    funding: str
    last4: int
    metadata: Dict[str, Any]
    name: str
    tokenization_method: str

    def __init__(self, id: str, object: str, address_city: None,
                 address_country: None, address_line1: None,
                 address_line1_check: None, address_line2: None,
                 address_state: None, address_zip: None,
                 address_zip_check: None, brand: str, country: str,
                 customer: str, cvc_check: str, dynamic_last4: None,
                 exp_month: int, exp_year: int, fingerprint: str, funding: str,
                 last4: int, metadata: Dict[str, Any], name: None,
                 tokenization_method: None) -> None:
        self.id = id
        self.object = object
        self.address_city = address_city
        self.address_country = address_country
        self.address_line1 = address_line1
        self.address_line1_check = address_line1_check
        self.address_line2 = address_line2
        self.address_state = address_state
        self.address_zip = address_zip
        self.address_zip_check = address_zip_check
        self.brand = brand
        self.country = country
        self.customer = customer
        self.cvc_check = cvc_check
        self.dynamic_last4 = dynamic_last4
        self.exp_month = exp_month
        self.exp_year = exp_year
        self.fingerprint = fingerprint
        self.funding = funding
        self.last4 = last4
        self.metadata = metadata
        self.name = name
        self.tokenization_method = tokenization_method


class ProductModel:
    id: str
    object: str
    active: bool
    attributes: List[str]
    created: int
    description: str
    images: List[Any]
    livemode: bool
    metadata: Dict[str, Any]
    name: str
    statement_descriptor: None
    type: str
    unit_label: None
    updated: int

    def __init__(self, id: str, object: str, active: bool,
                 attributes: List[str], created: int, description: str,
                 images: List[Any], livemode: bool, metadata: Dict[str, Any],
                 name: str, statement_descriptor: None, unit_label: None,
                 updated: int, type: str) -> None:
        self.id = id
        self.object = object
        self.active = active
        self.type = type
        self.attributes = attributes
        self.created = created
        self.description = description
        self.images = images
        self.livemode = livemode
        self.metadata = metadata
        self.name = name
        self.statement_descriptor = statement_descriptor
        self.unit_label = unit_label
        self.updated = updated


class PlanModel:
    id: str
    object: str
    active: bool
    aggregate_usage: None
    amount: int
    amount_decimal: int
    billing_scheme: str
    created: int
    currency: str
    interval: str
    interval_count: int
    livemode: bool
    metadata: Dict[str, Any]
    nickname: None
    product: str
    tiers_mode: None
    transform_usage: None
    trial_period_days: None
    usage_type: str

    def __init__(self, id: str, object: str, active: bool,
                 aggregate_usage: None, amount: int,
                 amount_decimal: int, billing_scheme: str, created: int,
                 currency: str, interval: str, interval_count: int,
                 livemode: bool, metadata: Dict[str, Any], nickname: None,
                 product: str, tiers_mode: None, transform_usage: None,
                 trial_period_days: None, usage_type: str) -> None:
        self.id = id
        self.object = object
        self.active = active
        self.aggregate_usage = aggregate_usage
        self.amount = amount
        self.amount_decimal = amount_decimal
        self.billing_scheme = billing_scheme
        self.created = created
        self.currency = currency
        self.interval = interval
        self.interval_count = interval_count
        self.livemode = livemode
        self.metadata = metadata
        self.nickname = nickname
        self.product = product
        self.tiers_mode = tiers_mode
        self.transform_usage = transform_usage
        self.trial_period_days = trial_period_days
        self.usage_type = usage_type


class RecurringModel:
    aggregate_usage: None
    interval: str
    interval_count: int
    trial_period_days: None
    usage_type: str

    def __init__(self, aggregate_usage: None, interval: str,
                 interval_count: int, trial_period_days: None,
                 usage_type: str) -> None:
        self.aggregate_usage = aggregate_usage
        self.interval = interval
        self.interval_count = interval_count
        self.trial_period_days = trial_period_days
        self.usage_type = usage_type


class PriceModel:
    id: str
    object: str
    active: bool
    billing_scheme: str
    created: int
    currency: str
    livemode: bool
    lookup_key: None
    metadata: Dict[str, Any]
    nickname: None
    product: str
    recurring: RecurringModel
    tiers_mode: None
    transform_quantity: None
    type: str
    unit_amount: int
    unit_amount_decimal: int

    def __init__(self, id: str, object: str, active: bool, billing_scheme: str,
                 created: int, currency: str, livemode: bool, lookup_key: None,
                 metadata: Dict[str, Any], nickname: None, product: str,
                 recurring: RecurringModel, tiers_mode: None,
                 transform_quantity: None, type: str, unit_amount: int,
                 unit_amount_decimal: int) -> None:
        self.id = id
        self.object = object
        self.active = active
        self.billing_scheme = billing_scheme
        self.created = created
        self.currency = currency
        self.livemode = livemode
        self.lookup_key = lookup_key
        self.metadata = metadata
        self.nickname = nickname
        self.product = product
        self.recurring = recurring
        self.tiers_mode = tiers_mode
        self.transform_quantity = transform_quantity
        self.type = type
        self.unit_amount = unit_amount
        self.unit_amount_decimal = unit_amount_decimal


class DatumPriceModel:
    id: str
    object: str
    billing_thresholds: None
    created: int
    metadata: Dict[str, Any]
    plan: PlanModel
    price: PriceModel
    quantity: int
    subscription: str
    tax_rates: List[Any]

    def __init__(self, id: str, object: str, billing_thresholds: None,
                 created: int, metadata: Dict[str, Any], plan: PlanModel,
                 price: PriceModel, quantity: int, subscription: str,
                 tax_rates: List[Any]) -> None:
        self.id = id
        self.object = object
        self.billing_thresholds = billing_thresholds
        self.created = created
        self.metadata = metadata
        self.plan = plan
        self.price = price
        self.quantity = quantity
        self.subscription = subscription
        self.tax_rates = tax_rates


class ItemsPriceModel:
    object: str
    data: List[DatumPriceModel]
    has_more: bool
    total_count: int
    url: str

    def __init__(self, object: str, data: List[DatumPriceModel],
                 has_more: bool, total_count: int, url: str) -> None:
        self.object = object
        self.data = [DatumPriceModel(**item) for item in data]
        self.has_more = has_more
        self.total_count = total_count
        self.url = url


class SubscriptionModel:
    id: str
    object: str
    application_fee_percent: None
    billing_cycle_anchor: int
    billing_thresholds: None
    cancel_at: None
    cancel_at_period_end: bool
    canceled_at: None
    collection_method: str
    created: int
    current_period_end: int
    current_period_start: int
    customer: str
    days_until_due: None
    default_payment_method: None
    default_source: None
    default_tax_rates: List[Any]
    discount: None
    ended_at: None
    items: ItemsModel
    latest_invoice: str
    livemode: bool
    metadata: Dict[str, Any]
    next_pending_invoice_item_invoice: None
    pause_collection: None
    pending_invoice_item_interval: None
    pending_setup_intent: None
    pending_update: None
    plan: PlanModel
    quantity: int
    schedule: None
    start_date: int
    status: str
    transfer_data: None
    trial_end: None
    trial_start: None

    def __init__(self, id: str, object: str, application_fee_percent: None,
                 billing_cycle_anchor: int, billing_thresholds: None,
                 cancel_at: None, cancel_at_period_end: bool,
                 canceled_at: None, collection_method: str,
                 created: int, current_period_end: int,
                 current_period_start: int, customer: str,
                 days_until_due: None, default_payment_method: None,
                 default_source: None, default_tax_rates: List[Any],
                 discount: None, ended_at: None, items: ItemsPriceModel,
                 latest_invoice: str, livemode: bool, metadata: Dict[str, Any],
                 next_pending_invoice_item_invoice: None,
                 pause_collection: None, pending_invoice_item_interval: None,
                 pending_setup_intent: None, pending_update: None,
                 plan: PlanModel, quantity: int, schedule: None,
                 start_date: int, status: str, transfer_data: None,
                 trial_end: None, trial_start: None) -> None:
        self.id = id
        self.object = object
        self.application_fee_percent = application_fee_percent
        self.billing_cycle_anchor = billing_cycle_anchor
        self.billing_thresholds = billing_thresholds
        self.cancel_at = cancel_at
        self.cancel_at_period_end = cancel_at_period_end
        self.canceled_at = canceled_at
        self.collection_method = collection_method
        self.created = created
        self.current_period_end = current_period_end
        self.current_period_start = current_period_start
        self.customer = customer
        self.days_until_due = days_until_due
        self.default_payment_method = default_payment_method
        self.default_source = default_source
        self.default_tax_rates = default_tax_rates
        self.discount = discount
        self.ended_at = ended_at
        self.items = items
        self.latest_invoice = latest_invoice
        self.livemode = livemode
        self.metadata = metadata
        self.next_pending_invoice_item_invoice = \
            next_pending_invoice_item_invoice
        self.pause_collection = pause_collection
        self.pending_invoice_item_interval = pending_invoice_item_interval
        self.pending_setup_intent = pending_setup_intent
        self.pending_update = pending_update
        self.plan = plan
        self.quantity = quantity
        self.schedule = schedule
        self.start_date = start_date
        self.status = status
        self.transfer_data = transfer_data
        self.trial_end = trial_end
        self.trial_start = trial_start


class SessionModel:
    id: str
    object: str
    created: int
    customer: str
    livemode: bool
    return_url: str
    url: str

    def __init__(self, id: str, object: str, created: int, customer: str,
                 livemode: bool, return_url: str, url: str) -> None:
        self.id = id
        self.object = object
        self.created = created
        self.customer = customer
        self.livemode = livemode
        self.return_url = return_url
        self.url = url
