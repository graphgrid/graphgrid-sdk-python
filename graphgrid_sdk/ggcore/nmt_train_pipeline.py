import math
import time

from graphgrid_sdk.ggcore.client import ConfigClient, NlpClient
from graphgrid_sdk.ggcore.config import SdkBootstrapConfig
from graphgrid_sdk.ggcore.sdk_messages import TrainRequestBody, PromoteModelResponse, NMTStatusResponse, \
    GetActiveModelResponse, NMTTrainPipelineResponse


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def evaluate_models(active_model: GetActiveModelResponse, new_model: NMTStatusResponse):
    active_model_data = active_model.trainedModelData
    if active_model_data.properties == new_model.properties:
        # Properties match (note: order matters for lists)
        # Now check if newer model has eval metrics
        if new_model.evalAccuracy is not None \
                and new_model.evalLoss is not None:
            # Does the other model have eval metrics too?
            if active_model_data.evalAccuracy is not None \
                    and active_model_data.evalLoss is not None:
                # Lower losses are preferred
                loss_delta = sigmoid(active_model_data.evalLoss) - \
                             sigmoid(new_model.evalLoss)
                # Higher accuracies are preferred
                acc_delta = -1 * (active_model_data.evalAccuracy - active_model_data.evalAccuracy)
                # The more positive, the better the model
                diff = loss_delta + acc_delta

                if diff >= 0:
                    # Update the selected model. Newer one is better
                    return new_model
                else:
                    return active_model
            else:
                # Choose more recent model with eval metrics
                return new_model

        elif active_model_data.trainingAccuracy is not None \
                and active_model_data.trainingLoss is not None \
                and new_model.trainingAccuracy is not None \
                and new_model.trainingLoss is not None:
            # Lower losses are preferred
            loss_delta = sigmoid(active_model_data.trainingLoss) - \
                         sigmoid(new_model.trainingLoss)
            # Higher accuracies are preferred
            acc_delta = -1 * (
                    active_model_data.trainingAccuracy - new_model.trainingAccuracy)
            # The more positive, the better the model
            diff = loss_delta + acc_delta

            if diff >= 0:
                # Update the selected model. Newer one is better
                return new_model
            else:
                return active_model

        elif active_model_data.evalLoss is not None \
                and new_model.evalLoss is not None:
            # This should only apply to translation
            if new_model.evalLoss <= active_model_data.evalLoss:
                return new_model
            else:
                return active_model

        else:
            # With no training or eval metrics choose more recent models
            return new_model
    else:
        # Properties do not match. Choose the newer model
        return new_model


class NmtTrainPipeline:
    _configuration: SdkBootstrapConfig

    _config_client: ConfigClient
    _nlp_client: NlpClient

    def __init__(self, bootstrap_config: SdkBootstrapConfig):
        self._configuration = bootstrap_config

        self._setup_clients()

    def _setup_clients(self):
        """Setup low-level clients."""
        self._config_client = ConfigClient(self._configuration)
        self._nlp_client = NlpClient(self._configuration)

    def nmt_train_pipeline(self, models_to_train, datasets, no_cache, gpu, autopromote, success_handler,
                           failed_handler):

        num_models = len(models_to_train)

        train_request_bodies = []
        for model in models_to_train:
            train_request_bodies.append(
                TrainRequestBody(model=model, datasets=datasets, no_cache=no_cache, gpu=gpu))

        nmt_train_responses = []
        for i in range(num_models):
            nmt_train_responses.append(self._nlp_client.trigger_nmt(train_request_bodies[i]))

        nmt_status_responses = []
        for i in range(num_models):
            nmt_status_responses.append(self._nlp_client.get_nmt_status(nmt_train_responses[i].dagRunId))

        completed_runs = 0
        while completed_runs < num_models:
            print("...running dag...")
            time.sleep(10)
            for status in nmt_status_responses:
                if status.state != "success" and status.state != "failed":
                    status_idx = nmt_status_responses.index(status)
                    nmt_status_responses[status_idx] = self._nlp_client.get_nmt_status(
                        nmt_train_responses[status_idx].dagRunId)
                    if nmt_status_responses[status_idx].state == "success" or \
                            nmt_status_responses[status_idx].state == "failed":
                        completed_runs = completed_runs + 1

        for model_status in nmt_status_responses:
            if model_status.state == "success" and success_handler is not None:
                success_handler(model_status)
            if model_status.state == "failed" and failed_handler is not None:
                failed_handler(model_status)

        print("Dag training/eval/model upload has finished.")

        promoted_models = []
        if autopromote:
            for i in range(num_models):
                status = nmt_status_responses[i]
                if status.state == "success":
                    selected_model = evaluate_models(self._nlp_client.get_active_model(models_to_train[i]),
                                                     status)  # should be task name, is model type as written (i.e. promote_model takes "task name" (e.g. named_entity_recognition), but we are giving it "model type" (e.g. "named-entity-recognition")
                    if selected_model == status:
                        promote_model_response: PromoteModelResponse = \
                            self._nlp_client.promote_model(status.savedModelName,
                                                           "default")  # should be task name, is model type as written (i.e. promote_model takes "task name" (e.g. named_entity_recognition), but we are giving it "model type" (e.g. "named-entity-recognition")
                        if promote_model_response.status_code == 200:
                            print("Model has been promoted.")
                            promoted_models.append(promote_model_response.modelName)
                        else:
                            print("Error promoting model: ", promote_model_response.exception)
                    else:
                        print("Model has not been promoted; currently active model has` greater accuracy")

            print("Model promotion is complete.")

        return NMTTrainPipelineResponse(nmt_status_responses, promoted_models)
