import pandas as pd
import datetime
import numpy as np


def total_tasks_weight(tasks_df: pd.DataFrame) -> pd.DataFrame:
    tasks_df = tasks_df.loc[:, ["shipment_id", "weight"]].groupby("shipment_id").sum()
    return tasks_df.rename(columns={"weight": "total_tasks_weight"})


def daily_tasks_total_weight_on_shipment(tasks_df: pd.DataFrame, date: datetime.date) -> int:
    is_todo_task_due_date = (tasks_df["status"] == "to_do") & (tasks_df["due_date"] == date)
    is_done_task_done_date = (tasks_df["status"] == "done") & (tasks_df["done_date"] == date)
    tasks_todo_today_on_shipment_df = tasks_df[(is_todo_task_due_date | is_done_task_done_date)]
    if len(tasks_todo_today_on_shipment_df["shipment_id"]) == 0:
        return 0
    daily_tasks_todo_total_weight_df = (
        tasks_todo_today_on_shipment_df.loc[:, ["shipment_id", "weight"]].groupby("shipment_id").sum()
    )
    return daily_tasks_todo_total_weight_df.weight.iat[0]


def shipment_total_workflows_weight(active_shipments_data_df: pd.DataFrame,) -> pd.DataFrame:
    shipment_total_workflows_weight_df: pd.DataFrame = active_shipments_data_df.loc[
        :, ["shipment_id", "total_workflow_weight"]
    ].groupby("shipment_id").sum()
    shipment_total_workflows_weight_df = shipment_total_workflows_weight_df.rename(
        columns={"total_workflow_weight": "total_workflows_weight"}
    )
    return shipment_total_workflows_weight_df


def find_shipment_workflow_start_date(active_shipments_data_df: pd.DataFrame) -> pd.DataFrame:
    active_shipments_data_df = active_shipments_data_df.groupby("shipment_id").min()
    active_shipments_data_df.loc[:, "workflow_associated_at"] = active_shipments_data_df[
        "workflow_associated_at"
    ].dt.date
    return active_shipments_data_df.rename(columns={"workflow_associated_at": "workflow_start_date"})


def shipments_remaining_days(active_shipments_data_df: pd.DataFrame, today: datetime.date) -> pd.DataFrame:
    active_shipments_data_df = active_shipments_data_df[
        [
            "shipment_id",
            "shipment_status",
            "freight_method",
            "freight_type",
            "foresea_name",
            "incoterm",
            "total_transit_time",
            "workflow_associated_at",
        ]
    ]
    shipments_with_start_dates_df = find_shipment_workflow_start_date(active_shipments_data_df)
    shipments_with_start_dates_df.loc[:, "remaining_days"] = (
        shipments_with_start_dates_df["total_transit_time"]
        - (today - shipments_with_start_dates_df["workflow_start_date"]).apply(lambda delta: delta.days)
        - 1
    )
    shipments_with_start_dates_df.loc[:, "remaining_days"] = shipments_with_start_dates_df["remaining_days"].clip(
        lower=0
    )
    return shipments_with_start_dates_df


def shipments_timelines(active_shipments_data_df: pd.DataFrame) -> pd.DataFrame:
    shipments_timelines_list = []
    for index, row in active_shipments_data_df.iterrows():
        shipment_timeline_df = pd.DataFrame(data={"shipment_id": [], "dates": []})
        start_date = row["workflow_start_date"]
        transit_time = row["total_transit_time"]
        dates = pd.date_range(start=start_date, periods=transit_time)
        shipment_timeline_df["dates"] = dates
        shipment_timeline_df["shipment_id"] = index
        shipments_timelines_list.append(shipment_timeline_df)
    shipments_timelines_df = pd.concat(shipments_timelines_list)
    shipments_timelines_df.loc[:, "dates"] = shipments_timelines_df["dates"].dt.date
    return shipments_timelines_df


def estimated_remaining_daily_workload(
    active_shipments_data_df: pd.DataFrame, tasks_df: pd.DataFrame, today: datetime.date,
) -> pd.DataFrame:
    shipment_total_workflows_weight_df = shipment_total_workflows_weight(
        active_shipments_data_df=active_shipments_data_df,
    )
    active_shipments_data_df = shipments_remaining_days(active_shipments_data_df, today)
    total_tasks_weight_df = total_tasks_weight(tasks_df=tasks_df)
    active_shipments_data_df = pd.merge(active_shipments_data_df, total_tasks_weight_df, on="shipment_id", how="left")
    active_shipments_data_df = pd.merge(
        active_shipments_data_df, shipment_total_workflows_weight_df, on="shipment_id", how="left"
    )
    active_shipments_data_df.loc[:, "estimated_remaining_daily_workload"] = (
        active_shipments_data_df["total_workflows_weight"] - active_shipments_data_df["total_tasks_weight"]
    ) / active_shipments_data_df["remaining_days"]
    active_shipments_data_df.loc[
        ~np.isfinite(active_shipments_data_df["estimated_remaining_daily_workload"]),
        "estimated_remaining_daily_workload",
    ] = 0
    return active_shipments_data_df


def daily_workload_calculation(shipments_timelines_df: pd.DataFrame, tasks_df: pd.DataFrame) -> pd.DataFrame:
    tasks_df.loc[:, "due_date"] = tasks_df["due_date"].dt.date
    tasks_df.loc[:, "done_date"] = tasks_df["done_date"].dt.date
    shipments_timelines_df.loc[:, "created_tasks_weight"] = shipments_timelines_df.apply(
        lambda row: daily_tasks_total_weight_on_shipment(
            tasks_df=tasks_df.loc[tasks_df["shipment_id"] == row["shipment_id"], :], date=row["dates"],
        ),
        axis=1,
    )
    shipments_timelines_df.loc[:, "daily_workload"] = (
        shipments_timelines_df["created_tasks_weight"] + shipments_timelines_df["estimated_remaining_daily_workload"]
    )
    return shipments_timelines_df


def shipments_daily_workload_timelines(
    active_shipments_data_df: pd.DataFrame, tasks_df: pd.DataFrame, today: datetime.date,
) -> pd.DataFrame:
    tasks_df.loc[:, "weight"] = tasks_df["weight"].fillna(0)
    active_shipments_data_df.loc[:, ["workflow_associated_at"]] = active_shipments_data_df[
        "workflow_associated_at"
    ].apply(lambda datestr: datetime.datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%fZ"))

    tasks_df = tasks_df.loc[:, ["shipment_id", "due_date", "status", "weight", "updated_at", "done_date"]]
    active_shipments_data_df = estimated_remaining_daily_workload(
        active_shipments_data_df=active_shipments_data_df, tasks_df=tasks_df, today=today,
    )
    shipments_timelines_df = shipments_timelines(active_shipments_data_df)
    shipments_timelines_df = pd.merge(shipments_timelines_df, active_shipments_data_df, how="left", on="shipment_id")
    shipments_timelines_df.loc[shipments_timelines_df["dates"] <= today, "estimated_remaining_daily_workload"] = 0.0
    shipments_timelines_df = daily_workload_calculation(
        shipments_timelines_df=shipments_timelines_df, tasks_df=tasks_df
    )
    return shipments_timelines_df[["shipment_id", "dates", "daily_workload"]]
