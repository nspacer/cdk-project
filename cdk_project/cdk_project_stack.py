from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_lambda as function,
    aws_lambda_event_sources as event_sources,
    aws_iam as iam,
    aws_dynamodb as dynamodb
)
from constructs import Construct


class CdkProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        dead_queue = sqs.Queue(
            self, "CdkDeadLetterQueue", queue_name='dead-letter-queue',
            visibility_timeout=Duration.seconds(300),
        )
        dead = sqs.DeadLetterQueue(max_receive_count=1,
                    queue=dead_queue)
        queue = sqs.Queue(
            self, "CdkProjectQueue", queue_name='lambda-queue',
            visibility_timeout=Duration.seconds(300),
            dead_letter_queue=dead
        )

        lambda_role = role = iam.Role(self, "DemoRole",
                                      assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        lambda_function = function.Function(self, "lambda_function",
                                            function_name="lambda_sqs",
                                            runtime=function.Runtime.PYTHON_3_9,
                                            timeout=Duration.minutes(3),
                                            code=function.Code.from_asset('lambda_code'),
                                            handler='sqs_lambda.lambda_handler',
                                            role=lambda_role)
        event_source = event_sources.SqsEventSource(queue)
        lambda_function.add_event_source(event_source)

        dynamodb.Table(self, "idTable", table_name="idTable",
                       partition_key=dynamodb.Attribute(
                           name="id",
                           type=dynamodb.AttributeType.STRING
                       )
                       )
