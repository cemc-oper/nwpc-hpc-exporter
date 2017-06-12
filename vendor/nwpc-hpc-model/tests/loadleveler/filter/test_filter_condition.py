import datetime
from nwpc_hpc_model.loadleveler.filter_condition import \
    FilterCondition, \
    PropertyFilterCondition, \
    create_equal_value_checker, \
    create_greater_value_checker, \
    create_less_value_checker, \
    create_in_value_checker


def create_job(
        job_id="id_no",
        owner="owner",
        job_class="job_class",
        queue_date=datetime.datetime.now(),
        status="R",
        priority=100
):
    return {
        "props": [
            {
                "id": "llq.id",
                "data": job_id,
                "text": job_id,
                "value": job_id
            },
            {
                "id": "llq.owner",
                "data": owner,
                "text": owner,
                "value": owner
            },
            {
                "id": "llq.class",
                "data": job_class,
                "text": job_class,
                "value": job_class
            },
            {
                "id": "llq.job_script",
                "data": "llq.job_script" + job_id,
                "text": "llq.job_script" + job_id,
                "value": "llq.job_script" + job_id
            },
            {
                "id": "llq.status" + job_id,
                "data": status,
                "text": status,
                "value": status
            },
            {
                "id": "llq.queue_date",
                "data": queue_date.strftime("%Y-%m-%d %H:%M:%S"),  # 2017-04-21 07:08:43
                "text": queue_date.strftime("%m/%d %H:%M"),  # "04/21 07:08",
                "value": queue_date.strftime("%a %b %d %H:%M:%S %Y"),  # "Fri Apr 21 07:08:43 2017"
            },
            {
                "id": "llq.priority",
                "data": priority,
                "text": priority,
                "value": priority
            }
        ]
    }


def test_condition():
    condition = FilterCondition()
    job_item = dict()
    assert condition.is_fit(job_item)


def test_equal_value_checker():
    job_item = create_job(job_id="id", owner="nwp_xp", job_class="serial", queue_date=datetime.datetime.now())

    condition = PropertyFilterCondition(
        property_id="llq.owner",
        data_checker=create_equal_value_checker("nwp_xp"))

    assert condition.is_fit(job_item)

    condition = PropertyFilterCondition(
        property_id="llq.owner",
        data_checker=create_equal_value_checker("unknown")
    )
    assert not condition.is_fit(job_item)


def test_greater_value_checker():
    job_item = create_job(
        job_id="id",
        owner="nwp_xp",
        job_class="serial",
        queue_date=datetime.datetime.now(),
        priority=100
    )
    condition = PropertyFilterCondition(
        property_id="llq.priority",
        data_checker=create_greater_value_checker(50))

    assert condition.is_fit(job_item)

    condition = PropertyFilterCondition(
        property_id="llq.priority",
        data_checker=create_greater_value_checker(100)
    )
    assert not condition.is_fit(job_item)


def test_less_value_checker():
    job_item = create_job(
        job_id="id",
        owner="nwp_xp",
        job_class="serial",
        queue_date=datetime.datetime.now(),
        priority=50
    )
    condition = PropertyFilterCondition(
        property_id="llq.priority",
        data_checker=create_less_value_checker(100))

    assert condition.is_fit(job_item)

    condition = PropertyFilterCondition(
        property_id="llq.priority",
        data_checker=create_less_value_checker(50)
    )
    assert not condition.is_fit(job_item)


def test_in_value_checker():
    job_item = create_job(
        job_id="id",
        owner="nwp_xp",
        job_class="serial",
        queue_date=datetime.datetime.now(),
        priority=50
    )
    condition = PropertyFilterCondition(
        property_id="llq.owner",
        data_checker=create_in_value_checker(("nwp_xp", "nwp", "nwp_qu")))

    assert condition.is_fit(job_item)

    condition = PropertyFilterCondition(
        property_id="llq.owner",
        data_checker=create_in_value_checker(("unknown",))
    )
    assert not condition.is_fit(job_item)
