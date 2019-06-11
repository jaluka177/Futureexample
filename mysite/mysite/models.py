# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Com(models.Model):
    com_name = models.CharField(primary_key=True, max_length=45)
    com_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'com'


class Company(models.Model):
    stockid = models.PositiveIntegerField(db_column='StockID', primary_key=True)  # Field name made lowercase.
    abbreviation = models.CharField(db_column='Abbreviation', unique=True, max_length=10, blank=True,
                                    null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', unique=True, max_length=128, blank=True,
                           null=True)  # Field name made lowercase.
    employees = models.PositiveIntegerField(db_column='Employees', blank=True, null=True)  # Field name made lowercase.
    capital = models.BigIntegerField(db_column='Capital', blank=True, null=True)  # Field name made lowercase.
    industryname = models.CharField(db_column='IndustryName', max_length=16)  # Field name made lowercase.
    listeddate = models.CharField(db_column='ListedDate', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company'


class Compiler(models.Model):
    category = models.CharField(primary_key=True, max_length=5)
    coding = models.TextField(blank=True, null=True)
    compiler_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'compiler'
        unique_together = (('category', 'compiler_name'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FutureBalancesheet(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    current_assets = models.CharField(max_length=15)
    cash_equivalents = models.CharField(max_length=15)
    inventory = models.CharField(max_length=15)
    non_current_assets = models.CharField(max_length=15)
    long_term_investment = models.CharField(max_length=15)
    fixed_assets = models.CharField(max_length=15)
    total_assets = models.CharField(max_length=15)
    current_liabilities = models.CharField(max_length=15)
    account_payable = models.CharField(max_length=15)
    non_current_liabilities = models.CharField(max_length=15)
    long_term_liabilities = models.CharField(max_length=15)
    total_liabilities = models.CharField(max_length=15)
    capital = models.CharField(max_length=15)
    total_equity = models.CharField(max_length=15)
    bps = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'future_balancesheet'


class FutureBalancesheetQ(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    current_assets = models.CharField(max_length=15)
    cash_equivalents = models.CharField(max_length=15)
    inventory = models.CharField(max_length=15)
    non_current_assets = models.CharField(max_length=15)
    long_term_investment = models.CharField(max_length=15)
    fixed_assets = models.CharField(max_length=15)
    total_assets = models.CharField(max_length=15)
    current_liabilities = models.CharField(max_length=15)
    account_payable = models.CharField(max_length=15)
    non_current_liabilities = models.CharField(max_length=15)
    long_term_liabilities = models.CharField(max_length=15)
    total_liabilities = models.CharField(max_length=15)
    capital = models.CharField(max_length=15)
    total_equity = models.CharField(max_length=15)
    bps = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'future_balancesheet_q'


class FutureCashFlows(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    income_before_tax = models.CharField(max_length=15)
    cf_operating_activities = models.CharField(db_column='CF_operating_activities', max_length=15)  # Field name made lowercase.
    cf_investing_activities = models.CharField(db_column='CF_investing_activities', max_length=15)  # Field name made lowercase.
    cf_financing_activities = models.CharField(db_column='CF_financing_activities', max_length=15)  # Field name made lowercase.
    net_cash_flows_accumulation = models.CharField(max_length=15)
    free_cash_flows = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'future_cash_flows'


class FutureCashFlowsQ(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    income_before_tax = models.CharField(max_length=15)
    cf_operating_activities = models.CharField(db_column='CF_operating_activities', max_length=15)  # Field name made lowercase.
    cf_investing_activities = models.CharField(db_column='CF_investing_activities', max_length=15)  # Field name made lowercase.
    cf_financing_activities = models.CharField(db_column='CF_financing_activities', max_length=15)  # Field name made lowercase.
    net_cash_flows = models.CharField(max_length=15)
    free_cash_flows = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'future_cash_flows_q'


class FutureCategory(models.Model):
    category_id = models.CharField(primary_key=True, max_length=2)
    category_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'future_category'


class FutureCna(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    time = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    source = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'future_cna'


class FutureComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    discuss_id = models.CharField(max_length=8)
    content = models.TextField()
    member_id = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'future_comment'


class FutureDiscuss(models.Model):
    discuss_id = models.AutoField(primary_key=True)
    theme = models.CharField(max_length=8)
    title = models.CharField(max_length=20)
    content = models.TextField()
    member_id = models.CharField(max_length=50)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    like = models.IntegerField(blank=True, null=True)
    reply_times = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'future_discuss'


class FutureDividendPolicy(models.Model):
    year = models.CharField(max_length=5)
    future_id = models.CharField(max_length=8)
    cash_dividend = models.CharField(max_length=15)
    stock_dividend = models.CharField(max_length=15)
    total_dividend = models.CharField(max_length=15)
    cash_dividend_ratio = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'future_dividend_policy'


class FutureEconomic(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    explain1 = models.TextField(blank=True, null=True)
    explain2 = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'future_economic'
        unique_together = (('id', 'category'),)


class FutureFq(models.Model):
    fq_id = models.CharField(max_length=2)
    fq_question = models.TextField()
    fq_choice1 = models.CharField(max_length=50)
    fq_choice2 = models.CharField(max_length=50)
    fq_choice3 = models.CharField(max_length=50)
    fq_choice4 = models.CharField(max_length=50, blank=True, null=True)
    fq_choice5 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'future_fq'


class FutureFqType(models.Model):
    type_id = models.CharField(primary_key=True, max_length=2)
    type_name = models.CharField(max_length=20)
    type_describe = models.TextField(blank=True, null=True)
    type_score = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'future_fq_type'


class FutureIncomeStatementQ(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    net_operating_revenues = models.CharField(max_length=15)
    net_gross_profit = models.CharField(max_length=15)
    operating_income = models.CharField(max_length=15)
    income_before_tax = models.CharField(max_length=15)
    net_income = models.CharField(max_length=15)
    eps = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'future_income_statement_q'


class FutureInformation(models.Model):
    future_id = models.CharField(primary_key=True, max_length=8)
    fu_name = models.CharField(max_length=12)
    fu_con_value = models.CharField(max_length=50)
    fu_min_lift = models.CharField(max_length=50)
    fu_last_tra = models.CharField(max_length=50)
    fu_fin_set_price = models.CharField(max_length=50)
    fu_u_d_limit = models.CharField(db_column='fu_u&d_limit',
                                    max_length=50)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'future_information'


class FutureMarketinformation(models.Model):
    market_id = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=10)
    index = models.CharField(max_length=10)
    buy_trans_num = models.CharField(max_length=10)
    buy_trading_volume = models.CharField(max_length=10)
    sell_trans_num = models.CharField(max_length=10)
    sell_trading_volume = models.CharField(max_length=10)
    trans_num = models.CharField(max_length=10)
    trading_volume = models.CharField(max_length=10)
    turnover_in_value = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'future_marketinformation'


class FutureMember(models.Model):
    member_id = models.AutoField(primary_key=True)
    member_name = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=12)
    type = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'future_member'


class FutureNewsIndex(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'future_news_index'


class FuturePe(models.Model):
    future_id = models.CharField(max_length=8)
    date = models.CharField(max_length=10)
    the_close = models.CharField(max_length=10)
    coporate_estimated = models.CharField(max_length=10)
    pe_for_four_season = models.CharField(max_length=10)
    pe_high = models.CharField(max_length=10)
    pe_low = models.CharField(max_length=10)
    eps = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'future_pe'


class FutureQuote1(models.Model):
    item = models.CharField(max_length=100, blank=True, null=True)
    finalprice = models.CharField(max_length=100, blank=True, null=True)
    amplitude = models.CharField(max_length=100, blank=True, null=True)
    updown = models.CharField(max_length=100, blank=True, null=True)
    open = models.CharField(max_length=100, blank=True, null=True)
    highest = models.CharField(max_length=100, blank=True, null=True)
    lowest = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'future_quote1'


class FutureRatio1(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    gross_margin = models.CharField(max_length=8)
    operating_profit_ratio = models.CharField(max_length=8)
    pretax_net_profit_margin = models.CharField(max_length=8)
    net_profit_margin = models.CharField(max_length=8)
    roe = models.CharField(db_column='ROE', max_length=8)  # Field name made lowercase.
    roa = models.CharField(db_column='ROA', max_length=8)  # Field name made lowercase.
    ps_sales = models.CharField(max_length=8)
    bps = models.CharField(max_length=8)
    eps = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'future_ratio1'


class FutureRatio1Q(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    gross_margin = models.CharField(max_length=8)
    operating_profit_ratio = models.CharField(max_length=8)
    pretax_net_profit_margin = models.CharField(max_length=8)
    net_profit_margin = models.CharField(max_length=8)
    roe = models.CharField(db_column='ROE', max_length=8)  # Field name made lowercase.
    roa = models.CharField(db_column='ROA', max_length=8)  # Field name made lowercase.
    ps_sales = models.CharField(max_length=8)
    bps = models.CharField(max_length=8)
    eps = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'future_ratio1_q'


class FutureRatio2Q(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    revenue_growth_ratio = models.CharField(max_length=8)
    operating_profit_growth_ratio = models.CharField(max_length=8)
    pretax_net_profit_growth_margin = models.CharField(max_length=8)
    net_profit_growth_margin = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'future_ratio2_q'


class FutureRatio3Q(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    accounts_receivable_turnover_ratio = models.CharField(max_length=8)
    accounts_payable_turnover_ratio = models.CharField(max_length=8)
    inventory_turnover_ratio = models.CharField(max_length=8)
    fixed_asset_turnover_ratio = models.CharField(max_length=8)
    total_asset_turnover_ratio = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'future_ratio3_q'


class FutureRatio4(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    current_ratio = models.CharField(max_length=8)
    quick_ratio = models.CharField(max_length=8)
    interest_cover = models.CharField(max_length=20)
    debt_ratio = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'future_ratio4'


class FutureRatio4Q(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    current_ratio = models.CharField(max_length=8)
    quick_ratio = models.CharField(max_length=8)
    interest_cover = models.CharField(max_length=20)
    debt_ratio = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'future_ratio4_q'


class FutureStockList(models.Model):
    list_id = models.CharField(max_length=15)
    list_name = models.CharField(max_length=15)
    member_id = models.CharField(max_length=15)
    context_id = models.CharField(max_length=4)
    context_ope = models.CharField(max_length=6)
    context_num = models.CharField(max_length=10)
    context = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'future_stock_list'


class FutureTechnologyIndex(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    day_k = models.CharField(db_column='day_K', max_length=8)  # Field name made lowercase.
    day_d = models.CharField(db_column='day_D', max_length=8)  # Field name made lowercase.
    day_macd = models.CharField(db_column='day_MACD', max_length=8)  # Field name made lowercase.
    day_rsi5 = models.CharField(db_column='day_RSI5', max_length=8)  # Field name made lowercase.
    day_rsi10 = models.CharField(db_column='day_RSI10', max_length=8)  # Field name made lowercase.
    week_k = models.CharField(db_column='week_K', max_length=8)  # Field name made lowercase.
    week_d = models.CharField(db_column='week_D', max_length=8)  # Field name made lowercase.
    week_macd = models.CharField(db_column='week_MACD', max_length=8)  # Field name made lowercase.
    week_rsi5 = models.CharField(db_column='week_RSI5', max_length=8)  # Field name made lowercase.
    week_rsi10 = models.CharField(db_column='week_RSI10', max_length=8)  # Field name made lowercase.
    month_k = models.CharField(db_column='month_K', max_length=8)  # Field name made lowercase.
    month_d = models.CharField(db_column='month_D', max_length=8)  # Field name made lowercase.
    month_macd = models.CharField(db_column='month_MACD', max_length=8)  # Field name made lowercase.
    month_rsi5 = models.CharField(db_column='month_RSI5', max_length=8)  # Field name made lowercase.
    month_rsi10 = models.CharField(db_column='month_RSI10', max_length=8)  # Field name made lowercase.
    q_k = models.CharField(db_column='q_K', max_length=8)  # Field name made lowercase.
    q_d = models.CharField(db_column='q_D', max_length=8)  # Field name made lowercase.
    q_rsi5 = models.CharField(db_column='q_RSI5', max_length=8)  # Field name made lowercase.
    q_rsi10 = models.CharField(db_column='q_RSI10', max_length=8)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'future_technology_index'


class FutureTechnologyIndex2(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    day_k = models.CharField(db_column='day_K', max_length=8)  # Field name made lowercase.
    day_d = models.CharField(db_column='day_D', max_length=8)  # Field name made lowercase.
    day_macd = models.CharField(db_column='day_MACD', max_length=8)  # Field name made lowercase.
    day_rsi5 = models.CharField(db_column='day_RSI5', max_length=8)  # Field name made lowercase.
    day_rsi10 = models.CharField(db_column='day_RSI10', max_length=8)  # Field name made lowercase.
    week_k = models.CharField(db_column='week_K', max_length=8)  # Field name made lowercase.
    week_d = models.CharField(db_column='week_D', max_length=8)  # Field name made lowercase.
    week_macd = models.CharField(db_column='week_MACD', max_length=8)  # Field name made lowercase.
    week_rsi5 = models.CharField(db_column='week_RSI5', max_length=8)  # Field name made lowercase.
    week_rsi10 = models.CharField(db_column='week_RSI10', max_length=8)  # Field name made lowercase.
    month_k = models.CharField(db_column='month_K', max_length=8)  # Field name made lowercase.
    month_d = models.CharField(db_column='month_D', max_length=8)  # Field name made lowercase.
    month_macd = models.CharField(db_column='month_MACD', max_length=8)  # Field name made lowercase.
    month_rsi5 = models.CharField(db_column='month_RSI5', max_length=8)  # Field name made lowercase.
    month_rsi10 = models.CharField(db_column='month_RSI10', max_length=8)  # Field name made lowercase.
    q_k = models.CharField(db_column='q_K', max_length=8)  # Field name made lowercase.
    q_d = models.CharField(db_column='q_D', max_length=8)  # Field name made lowercase.
    q_rsi5 = models.CharField(db_column='q_RSI5', max_length=8)  # Field name made lowercase.
    q_rsi10 = models.CharField(db_column='q_RSI10', max_length=8)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'future_technology_index2'


class FutureTrackFuture(models.Model):
    member_id = models.CharField(max_length=10)
    future_id = models.CharField(max_length=10, blank=True, null=True)
    list_id = models.CharField(max_length=5, blank=True, null=True)
    list_name = models.CharField(max_length=10, blank=True, null=True)
    future_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'future_track_future'


class FutureTrade2015(models.Model):
    date = models.CharField(max_length=20)
    sell_stock = models.CharField(max_length=20)
    sell_price = models.CharField(max_length=20)
    stocks = models.CharField(max_length=10)
    net = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'future_trade_2015'


class FutureTransactionInfo(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    the_open = models.CharField(max_length=8)
    high_price = models.CharField(max_length=8)
    low_price = models.CharField(max_length=8)
    the_close = models.FloatField()
    change = models.FloatField()
    change_percent = models.CharField(max_length=8)
    vol = models.FloatField()

    class Meta:
        managed = False
        db_table = 'future_transaction_info'


class FutureTransactionInfo2(models.Model):
    date = models.CharField(max_length=10)
    future_id = models.CharField(max_length=8)
    the_open = models.CharField(max_length=8)
    high_price = models.CharField(max_length=8)
    low_price = models.CharField(max_length=8)
    the_close = models.FloatField()
    change = models.FloatField()
    change_percent = models.CharField(max_length=8)
    vol = models.FloatField()
    stock_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'future_transaction_info_2'


class FutureType(models.Model):
    future_id = models.IntegerField(blank=True, null=True)
    future_name = models.CharField(primary_key=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'future_type'


class FutureYahoo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    source = models.CharField(max_length=20)
    time = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'future_yahoo'


class FutureYahooGlobal(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'future_yahoo_global'


class FutureYahooHot(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)
    tag = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'future_yahoo_hot'


class FutureYahooInfo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'future_yahoo_info'


class FutureYahooNew(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    source = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'future_yahoo_new'


class FutureYahooStock(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)
    tag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'future_yahoo_stock'


class FutureYahooTec(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)
    tag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'future_yahoo_tec'


class FutureYahooTendency(models.Model):
    category = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=10)
    source = models.CharField(max_length=20)
    tag0 = models.CharField(max_length=10, blank=True, null=True)
    tag1 = models.CharField(max_length=10, blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    img_source = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'future_yahoo_tendency'


class FutureYahooTra(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    source = models.CharField(max_length=20)
    tag = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'future_yahoo_tra'


class FuturesQuote(models.Model):
    item = models.CharField(max_length=10, blank=True, null=True)
    finalprice = models.CharField(max_length=100, blank=True, null=True)
    amplitude = models.CharField(max_length=100, blank=True, null=True)
    updown = models.CharField(max_length=100, blank=True, null=True)
    open = models.CharField(max_length=100, blank=True, null=True)
    highest = models.CharField(max_length=100, blank=True, null=True)
    lowest = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'futures_quote'


class FuturesQuote1(models.Model):
    item = models.CharField(max_length=100, blank=True, null=True)
    finalprice = models.CharField(max_length=100, blank=True, null=True)
    amplitude = models.CharField(max_length=100, blank=True, null=True)
    updown = models.CharField(max_length=100, blank=True, null=True)
    open = models.CharField(max_length=100, blank=True, null=True)
    highest = models.CharField(max_length=100, blank=True, null=True)
    lowest = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'futures_quote1'
