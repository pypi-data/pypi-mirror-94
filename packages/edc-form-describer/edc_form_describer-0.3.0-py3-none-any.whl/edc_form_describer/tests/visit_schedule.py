from dateutil.relativedelta import relativedelta
from edc_visit_schedule import Crf, FormsCollection, Schedule, Visit, VisitSchedule

crfs = FormsCollection(
    Crf(show_order=1, model="edc_fieldsets.mymodel", required=True),
    Crf(show_order=2, model="edc_fieldsets.mymodel2", required=True),
    Crf(show_order=3, model="edc_fieldsets.mymodel3", required=True),
)


visit0 = Visit(
    code="1000",
    title="Day 1",
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    crfs=crfs,
    facility_name="default",
)

visit1 = Visit(
    code="2000",
    title="Day 2",
    timepoint=1,
    rbase=relativedelta(days=1),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    crfs=crfs,
    facility_name="default",
)

schedule = Schedule(
    name="schedule",
    onschedule_model="edc_visit_schedule.onschedule",
    offschedule_model="edc_visit_schedule.offschedule",
    appointment_model="edc_appointment.appointment",
    consent_model="edc_consent.subjectconsent",
)

schedule.add_visit(visit0)
schedule.add_visit(visit1)

visit_schedule = VisitSchedule(
    name="visit_schedule",
    offstudy_model="edc_offstudy.subjectoffstudy",
    death_report_model="edc_adverse_event.deathreport",
)

visit_schedule.add_schedule(schedule)
