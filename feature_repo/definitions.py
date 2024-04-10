from feast import Entity
from feast.feature_view import FeatureView
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import \
    PostgreSQLSource

task = Entity(name="task", join_keys=["task_id"])

TASK_COLUMNS = """
id AS task_id,
created_at, updated_at AS event_timestamp, is_labeled, project_id, inner_id,
total_annotations, cancelled_annotations, total_predictions
"""
TASK_TRANSFORMED_COLUMNS = """
data->>'image' as image
"""

tasks_source = PostgreSQLSource(
    name="labelstudio_tasks",
    query=f"SELECT {TASK_COLUMNS}, {TASK_TRANSFORMED_COLUMNS} FROM task",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_at",
)

ANNOTATION_QUERY = """SELECT
	-- task_completion attributes
	id AS annotation_id,
	tc.was_cancelled, tc.ground_truth, tc.created_at, tc.updated_at AS event_timestamp, tc.task_id,
	-- task_completion.result fields
	annotation->>'type' as type,
	annotation->>'id' as region_id,
	annotation->>'from_name' as from_name,
	annotation->>'to_name' as to_name,
	CAST(annotation->>'original_width' AS INTEGER) as original_width,
	CAST(annotation->>'original_height' AS INTEGER) as original_height,
	annotation->>'origin' as origin,
	CAST(annotation->>'image_rotation' AS DOUBLE PRECISION) as image_rotation,
	CAST(annotation->>'score' AS DOUBLE PRECISION) as score,
	-- task_completion.result->[]->value
	annotation->'value'->>'points' as points,
	CAST(annotation->'value'->>'closed' AS BOOLEAN) as closed,
	ARRAY(SELECT jsonb_array_elements_text(annotation->'value'->'choices')) as choices,
	CAST(annotation->'value'->>'x' AS DOUBLE PRECISION) as x,
	CAST(annotation->'value'->>'y' AS DOUBLE PRECISION) as y,
	CAST(annotation->'value'->>'width' AS DOUBLE PRECISION) as width,
	CAST(annotation->'value'->>'height' AS DOUBLE PRECISION) as height,
	CAST(annotation->'value'->>'rotation' AS DOUBLE PRECISION) as rotation,
	ARRAY(SELECT jsonb_array_elements_text(annotation->'value'->'polygonlabels')) as polygonlabels,
	ARRAY(select jsonb_array_elements_text(annotation->'value'->'rectanglelabels')) as rectanglelabels
from
	task_completion tc,
	LATERAL jsonb_array_elements(tc.result) as annotation
"""

annotations_source = PostgreSQLSource(
    name="labelstudio_annotations",
    query=ANNOTATION_QUERY,
    timestamp_field="event_timestamp",
    created_timestamp_column="created_at",
)

tasks_view = FeatureView(
    name="tasks",
    entities=[task],
    source=tasks_source,
)

annotations_view = FeatureView(
    name="annotations",
    entities=[task],
    source=annotations_source,
)