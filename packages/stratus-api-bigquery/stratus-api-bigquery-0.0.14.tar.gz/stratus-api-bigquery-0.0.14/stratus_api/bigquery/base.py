client = None


def extract_attributes(body: dict) -> tuple:
    """Convenience function to extract common attributes from PubSub messages

    :param body:
    :return: Tuple of external_id, external service name, and the promise results
    """
    import base64, json
    message = body.get('message', dict())
    attributes = message.get('attributes', dict())
    service_name = 'bigquery'
    results = json.loads(base64.b64decode(message['data']).decode('utf-8'))
    output = results['protoPayload']['serviceData']['jobCompletedEvent']['job']['jobStatistics']
    external_id = results['protoPayload']['serviceData']['jobCompletedEvent']['job']['jobName']['jobId']
    status = 'completed'
    if results['protoPayload']['serviceData']['jobCompletedEvent']['job']['jobStatus'].get('error'):
        status = 'failed'
        output = dict(
            error=results['protoPayload']['serviceData']['jobCompletedEvent']['job']['jobStatus']['error'])
    return external_id, service_name, status, output


def process_promise_update_request(body):
    from stratus_api.jobs.tasks.promises import update_promise_task
    from stratus_api.jobs.base import start_task_signature
    external_id, service_name, status, results = extract_attributes(body=body)
    sig = update_promise_task.s(status=status, service_name=service_name, external_id=external_id, results=results)
    start_task_signature(sig=sig)
    return dict(active=True)
