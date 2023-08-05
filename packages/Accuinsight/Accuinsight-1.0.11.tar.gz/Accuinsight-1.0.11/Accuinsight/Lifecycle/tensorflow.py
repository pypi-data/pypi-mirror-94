import os
import sys
import inspect
import json
import logging
import warnings
from pathlib import Path
import datetime 
from collections import OrderedDict

import boto3
import gorilla
import pymysql
from slack import WebClient
from slack.errors import SlackApiError

import numpy as np
import tensorflow
from tensorflow.keras.callbacks import CSVLogger
from Accuinsight.modeler.core import func, path, get
from Accuinsight.modeler.core.func import get_time
from Accuinsight.modeler.core.LcConst import LcConst
from Accuinsight.modeler.core.LcConst.LcConst import RUN_NAME_TENSORFLOW, ENV_JUPYTER_HOME_DIR 
from Accuinsight.modeler.core.Run.RunInfo.RunInfo import set_current_runs, clear_runs, set_model_json_path, \
    set_visual_csv_path, set_visual_json_path, set_best_model_json_path, set_best_model_h5_path, print_run_info, \
    set_python_dependencies, set_run_name, set_model_file_path, set_prefix_path, set_shap_json_path 
from Accuinsight.modeler.core.get_for_visual import roc_pr_curve, get_true_y, get_visual_info_regressor
from Accuinsight.modeler.clients.modeler_api import LifecycleRestApi
from Accuinsight.modeler.utils.dependency.dependencies import gather_sources_and_dependencies
from Accuinsight.modeler.utils.dl_utils import delete_files_except_best, get_best_model_path
from Accuinsight.modeler.utils.os_getenv import is_in_ipython, get_current_notebook
from Accuinsight.modeler.utils.runs_utils import get_aws_info, ProgressPercentage
from Accuinsight.modeler.core.feature_contribution import shap_value

logging.basicConfig(level=logging.INFO,
                    format='%(message)s')

warnings.filterwarnings("ignore")


class accuinsight(object):
    def __init__(self):
        self.BucketInfo = None
        self.target_name = None
        self.save_path = None
        self.endpoint = None
        self.thresholds = None
        self.token = None
        self.channel_id = None
        self.message = None

    def get_file(self, aws_json_file_name):
        
        # meta file 저장하는 폴더 만들면, 이 경로는 수정돼야 함.
        aws_info_json_path = os.path.join(ENV_JUPYTER_HOME_DIR, aws_json_file_name)
       
        with open(aws_info_json_path) as jsonFile:
            self.BucketInfo = json.load(jsonFile)
            
        BUCKET_TYPE = self.BucketInfo['bucketType']
        BUCKET_NAME = self.BucketInfo['bucketName']
        FILE_PATH = self.BucketInfo['filePath']
        FILE_NAME = self.BucketInfo['fileName']
        #FILE_TYPE = self.BucketInfo['fileType']
        #FILE_DELIM = self.BucketInfo['fileDelim']
        ACCESS_KEY = self.BucketInfo['myAccessKey']
        SECRET_KEY = self.BucketInfo['mySecretKey']
        REGION = self.BucketInfo['region']
        URL = self.BucketInfo['endpoint']
        
        ## define the target name 
        self.target_name = self.BucketInfo['target']

        ## path for saving data
        save_dir = os.path.join(ENV_JUPYTER_HOME_DIR, 'data_from_AWS')
        if os.path.exists(save_dir) == False:
            os.mkdir(save_dir)
        else:
            pass
        
        self.save_file_name = FILE_NAME.split('.')[0] + '_' + str(datetime.datetime.now().date()).replace('-', '') + '.' + FILE_NAME.split('.')[1]
        self.save_path = os.path.join(save_dir, self.save_file_name)

        # endpoint
        pre_url = 'https://' + BUCKET_NAME + '.' + URL
        self.endpoint = os.path.join(pre_url, FILE_PATH)

        client = boto3.client(BUCKET_TYPE,
                              aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY,
                              region_name=REGION)

        transfer = boto3.s3.transfer.S3Transfer(client)

        progress = ProgressPercentage(client, BUCKET_NAME, FILE_PATH)

        sys.stdout.write('%s %s %s' % ('Downloading file...', FILE_NAME, '\n'))
        transfer.download_file(BUCKET_NAME, FILE_PATH, self.save_path, callback=progress)
        logging.info(self.save_path)
    
   # def get_feature_name(self):
   #     fileType = self.BucketInfo['fileName'].split('.')[0]
   #     if fileType == 'json':
   #         with open(self.save_path) as jsonFile:
   #             json_data = json.load(jsonFile)
   #         self.feature_name = json_data.keys()
   #     elif fileType == 'csv':
   #         self.feature_name = list(pd.read_csv(self.save_path).columns)
   #         if 'Unnamed: 0' in feature_list:
   #             self.feature_name.remove('Unnamed: 0')
   #     else:
   #         logging.info('현재 지원하는 데이터 형식은 json(key: feature name)과 csv입니다.\n feature name을 가져올 수 없는 경우, [feature_1, feature_2, ...]과 같이 임의로 할당합니다.')
   #     return(self.feature_name)
    
    def set_slack(self, token=None, channel_id=None):
        self.token = token
        self.channel_id = channel_id

    def send_message(self, message=None, thresholds=None):
        if message is not None and thresholds is not None:
            raise ValueError("'message'와 'thresholds' 두 개의 arguments를 동시에 입력할 수 없습니다.")
        else:
            self.message = message
            self.thresholds = thresholds

    def autolog(self, tag=None, best_weights = False, model_monitor=False):
        global description, endpoint, var_model_file_path, message, thresholds, token, channel_id, best_weights_on, \
               feature_name, run_id, shap_on
        description = tag
        endpoint = self.endpoint
        message = self.message
        thresholds = self.thresholds
        token = self.token
        channel_id = self.channel_id
    
        if best_weights == True:
            best_weights_on = True
        else:
            best_weights_on = False
        if model_monitor == True:
            shap_on = True
            try:
                feature_name = get.feature_name(self.save_path, self.BucketInfo, self.target_name)
            except:
                feature_name = None      # when user did not using <get_file> function     
        else:
            shap_on = False
        run_id = None
        
        
        
#         print(feature_name)   ####################################################

        is_notebook = is_in_ipython()
        if is_notebook == True:
            var_model_file_path = get_current_notebook()
            _caller_globals = inspect.stack()[1][0].f_globals
            (
                mainfile,
                sources,
                dependencies
            ) = gather_sources_and_dependencies(
                globs=_caller_globals,
                save_git_info=False
            )
        else:
            _caller_globals = inspect.stack()[1][0].f_globals
            (
                mainfile,
                sources,
                dependencies
            ) = gather_sources_and_dependencies(
                globs=_caller_globals,
                save_git_info=True
            )
            var_model_file_path = mainfile['filename']

        class TrainHistoryCallbacks(tensorflow.keras.callbacks.Callback):
            def __init__(self, verbose=1, mode='auto'):
                super(TrainHistoryCallbacks, self).__init__()
                self.verbose = verbose
                self.best_epochs = 0
                self.epochs_since_last_save = 0
                self.mode = mode

            def on_train_begin(self, logs={}):
                if best_weights_on and shap_on:
                    logging.info('Using autolog(best_weights=True, model_monitor=True)')
                elif best_weights_on == True and shap_on == False:
                    logging.info('Using autolog(best_weights=True, model_monitor=False)')
                elif best_weights_on == False and shap_on == True:
                    logging.info('Using autolog(best_weights=False, model_monitor=True)')
                else:
                    logging.info('Using autolog(best_weights=False, model_monitor=False)')
                
                global start
                start = get_time.now()
                opt = self.model.optimizer.get_config()
                opt_key = list(opt.keys())[1:]
                opt_result = {k: np.float64(opt[k]) for k in opt_key}
                self.model_summary = OrderedDict()
                self.model_summary['data_version'] = endpoint
                self.model_summary['model_description'] = description
                self.model_summary['logging_time'] = get_time.logging_time()
                self.model_summary['run_id'] = func.get_run_id()
                self.model_summary['model_type'] = get.model_type(self.model)

                if hasattr(self.model.loss, 'get_config'):
                    self.model_summary['loss_function'] = self.model.loss.get_config()['name']
                else:
                    self.model_summary['loss_function'] = self.model.loss

                self.model_summary['optimizer_info'] = {opt['name']: opt_result}

                '''[get best model] on_train_begin '''
                self.best_weights = self.model.get_weights()

                self.dict_path = path.get_file_path(self.model, usedFramework='tensorflow')

                set_prefix_path(self.dict_path[LcConst.RUN_PREFIX_PATH])

                set_run_name(self.model_summary['model_type'], self.model_summary['run_id'])
                set_python_dependencies(py_depenpency=dependencies)

#                print('dict_path: ', self.dict_path)         ######################
        
            '''[get best model] on_epoch_end '''
            def on_epoch_end(self, epoch, logs=None):
                logs = logs or {}
                if epoch == 0:
                    if len(self.model.metrics_names) == 1 and 'loss' in self.model.metrics_names:
                        self.monitor = 'val_loss'
                    elif len(self.model.metrics_names) >= 2:
                        self.monitor = 'val_' + self.model.metrics_names[1]
                    # set monitoring option
                    if self.mode not in ['auto', 'min', 'max']:
                        warnings.warn('GetBest mode %s is unknown, '
                                      'fallback to auto mode.' % (self.mode), RuntimeWarning)
                        self.mode = 'auto'
                    if self.mode == 'min':
                        self.monitor_op = np.less
                        self.best = np.Inf
                    elif self.mode == 'max':
                        self.monitor_op = np.greater
                        self.best = -np.Inf
                    else:
                        if 'acc' in self.monitor or 'f1' in self.monitor:
                            self.monitor_op = np.greater
                            self.best = -np.Inf
                        else:
                            self.monitor_op = np.less
                            self.best = np.Inf
                else:
                    pass
                
                # Using best_weights
                if best_weights_on:
                    
                    # update best_weights
                    self.epochs_since_last_save += 1
                    if self.epochs_since_last_save >= 1:
                        self.epochs_since_last_save = 0
                        current = logs.get(self.monitor)
                        if current is None:
                            warnings.warn('Can pick best model only with %s available, '
                                      'skipping.' % (self.monitor), RuntimeWarning)
                        else:
                            if self.monitor_op(current, self.best):
#                                 if self.verbose > 0:
#                                     print('\n\nEpoch %05d: %s improved from %0.5f to %0.5f,'
#                                           ' storing weights.\n'
#                                           % (epoch + 1, self.monitor, self.best, current))
                                self.best = current
                                self.best_epochs = epoch + 1
                                self.best_weights = self.model.get_weights()
                            else:
                                pass
#                                 if self.verbose > 0:
#                                     print('\n\nEpoch %05d: %s did not improve\n' % (epoch + 1, self.monitor))

                    self.current_value = current
    
                # Not using best_weights
                else:
                    self.last_epoch_metric = logs.get(self.monitor)
                    self.best_epochs = epoch + 1
                    current = logs.get(self.monitor)
                    self.current_value = current

                # model save path
                run_id = self.model_summary['model_type'] + '-' + self.model_summary['run_id']
                common_path = self.dict_path['save_model_path'] + run_id + '-epoch-' + str(epoch + 1).zfill(5) + '-' + self.monitor + '-' + str(current).zfill(5)
                save_model_path = common_path + '.json'
                save_weights_path = common_path + '.h5'
                # model to JSON
                model_json = self.model.to_json()
                with open(save_model_path, "w") as json_file:
                    json_file.write(model_json)
                # weights to H5
                self.model.save_weights(save_weights_path)


            def on_train_end(self, logs={}):
                '''[get best model] on_train_end '''
                if best_weights_on:
                    if self.verbose > 0:
                        print('\nUsing epoch %05d with %s: %0.5f' % (self.best_epochs, self.monitor, self.best))
                    self.model.set_weights(self.best_weights)  # set best model's weights
                    
                    self.model_summary['selected_metrics'] = {self.monitor: np.float64(self.best)}
                else:
                    self.model_summary['selected_metrics'] = {self.monitor: np.float64(self.last_epoch_metric)}
    
          #      print('model_summary: ', self.model_summary)   ##############################
                end = get_time.now()
                self.model_summary['time_delta'] = str(end - start)

                # path for model_info.json
                self.path_for_setting_model_json = self.dict_path['model_json']
                set_model_json_path(self.path_for_setting_model_json)

                model_json_full_path = self.dict_path['model_json_full']

                with open(model_json_full_path, 'w', encoding='utf-8') as save_file:
                    json.dump(self.model_summary, save_file, indent="\t")

                delete_files_except_best(run_id=self.model_summary['run_id'], epochs=str(self.best_epochs),
                                         path=self.dict_path)

                path_for_setting_model_json = self.dict_path['save_model_dir'] + \
                                              get_best_model_path(run_id=self.model_summary['run_id'],
                                                                  path=self.dict_path)['json']
                path_for_setting_model_h5 = self.dict_path['save_model_dir'] + \
                                            get_best_model_path(run_id=self.model_summary['run_id'],
                                                                path=self.dict_path)['h5']
                set_best_model_json_path(path_for_setting_model_json)
                set_best_model_h5_path(path_for_setting_model_h5)

                start_ts = int(start.timestamp())
                end_ts = int(end.timestamp())
                delta_ts = end_ts - start_ts

                clear_runs(start_ts, end_ts, delta_ts)
#                 accuinsight._send_message(metric=self.monitor,
#                                           current_value=self.current_value,
#                                           message=message,
#                                           thresholds=thresholds,
#                                           token=token,
#                                           channel_id=channel_id)
                modeler_rest = LifecycleRestApi(LcConst.BACK_END_API_URL,
                                                LcConst.BACK_END_API_PORT,
                                                LcConst.BACK_END_API_URI)
                modeler_rest.lc_create_run()
                accuinsight._off_autolog()

        class visualCallbacks(tensorflow.keras.callbacks.Callback):
            def __init__(self, x_validation=None, y_validation=None):
                self.x_val = x_validation
                self.y_val = y_validation

            def on_train_end(self, logs={}):

                self.dict_path = path.get_file_path(self.model, usedFramework='tensorflow')
                # path for visual.json
                path_for_setting_visual_json = self.dict_path['visual_json']
                visual_json_full_path = self.dict_path['visual_json_full']
                set_visual_json_path(path_for_setting_visual_json)

                # classification
                if get.is_classification(self.model):
                    visual_classification_json = roc_pr_curve(self.model, self.x_val, self.y_val)

                    with open(visual_json_full_path, 'w', encoding='utf-8') as save_file:
                        json.dump(visual_classification_json, save_file, indent="\t")

                # regression
                else:
                    visual_regression_json = OrderedDict()
                    visual_regression_json['True_y'] = get_true_y(self.y_val)
                    visual_regression_json['Predicted_y'] = get_visual_info_regressor(self.model, self.x_val)

                    with open(visual_json_full_path, 'w', encoding='utf-8') as save_file:
                        json.dump(visual_regression_json, save_file, indent="\t")
        

        class shapCallbacks(tensorflow.keras.callbacks.Callback):
            def __init__(self, trainX, feature_name, run_id, trigger = shap_on):
                self.trainX = trainX
                self.trigger = shap_on
                self.run_id = run_id
                #if feature_name is not None:
                #    self.feature_name = feature_name
                #else:
                self.feature_name = feature_name
                

            def on_train_end(self, logs={}):
                if self.trigger:
                    self.shap_value = shap_value(self.model, self.trainX, self.feature_name)
                
#                    print('shap_value')   ##################
#                    print(self.shap_value)   ##################
                    
#                     func.insertDB(self.shap_value, 2)  # 수정: 2 -> self.run_id
                    
                    self.dict_path = path.get_file_path(self.model, usedFramework='tensorflow')

                    # path for shap.json
                    shap_json_full_path = self.dict_path['shap_json_full']
                    set_shap_json_path(self.dict_path['shap_json'])
                    
                    with open(shap_json_full_path, 'w', encoding='utf-8') as save_file:
                        json.dump(self.shap_value, save_file, indent='\t')

                else:
                    pass    
                    
        def run_and_log_function(self, original, x, y, kwargs):
            dict_path = path.get_file_path(self, usedFramework='tensorflow')
            path_for_setting_visual_csv = dict_path['visual_csv']
            visual_csv_full_path = dict_path['visual_csv_full']

            # set current run
            set_current_runs(RUN_NAME_TENSORFLOW)
            set_model_file_path(var_model_file_path)
            set_visual_csv_path(path_for_setting_visual_csv)

            csv_logger = CSVLogger(visual_csv_full_path, append=True, separator=';')
            
            # get train data(x) for computing shap value
            if 'x':
                x_train = x
            if shap_on:
#                print('using model_monitor_1')
                get_shap = shapCallbacks(x_train, feature_name, run_id, trigger = shap_on)
            else:
#                print('not using model_monitor_1')
                pass
            
            ''' save json for visualization '''
            # using validation_data argument
            if 'validation_data' in kwargs:
                validation_set = kwargs['validation_data']

                try:
                    x_val = validation_set[0]
                    y_val = validation_set[1]

                except:
                    iterator = iter(validation_set)
                    valid_set = next(iterator)
                    x_val = valid_set[0].numpy()
                    y_val = valid_set[1].numpy()

                get_visual = visualCallbacks(x_validation=x_val, y_validation=y_val)

            else:
                raise ValueError('"validation_data" does not exist.')

            if 'callbacks' in kwargs:
                kwargs['callbacks'] += [csv_logger]
                kwargs['callbacks'] += [get_visual]
                if shap_on:
                    kwargs['callbacks'] += [get_shap]
                else:
                    pass
                kwargs['callbacks'] += [TrainHistoryCallbacks()]
                

            else:
                kwargs['callbacks'] = [csv_logger]
                kwargs['callbacks'] += [get_visual]
                if shap_on:
                    kwargs['callbacks'] += [get_shap]
                else:
                    pass
                kwargs['callbacks'] += [TrainHistoryCallbacks()]
                


            fit_model = original(self, x, y, **kwargs)
            return (fit_model)

        @gorilla.patch(tensorflow.keras.Model)
        def fit(self, x, y, **kwargs):
            original = gorilla.get_original_attribute(tensorflow.keras.Model, 'fit')
            unlogged_params = ['self', 'callbacks', 'validation_data', 'verbose']
            return run_and_log_function(self, original, x, y, kwargs)

        settings = gorilla.Settings(allow_hit=True, store_hit=True)
        gorilla.apply(gorilla.Patch(tensorflow.keras.Model, 'fit', fit, settings=settings))

    def _send_message(metric=None, current_value=None, message=None, thresholds=None, token=None, channel_id=None):
        if token is not None and channel_id is not None:
            if thresholds is not None:
                try:
                    if current_value >= thresholds:
                        msg = '[모델 학습 완료] ' + metric + '이 설정하신 thresolds: ' + str(thresholds) + '를 초과하였습니다.'
                        response = WebClient(token=token).chat_postMessage(channel=channel_id, text=msg)
                except SlackApiError as e:
                    assert e.response["error"]
            elif message is not None:
                try:
                    msg = message
                    response = WebClient(token=token).chat_postMessage(channel=channel_id, text=msg)
                except SlackApiError as e:
                    assert e.response["error"]
        else:
            pass

    def _off_autolog():
        def stop_log(self, original, args, kwargs, unlogged_params):
            fit_model = original(self, *args, **kwargs)
            return (fit_model)

        @gorilla.patch(tensorflow.keras.Model)
        def fit(self, *args, **kwargs):
            original = gorilla.get_original_attribute(tensorflow.keras.Model, 'fit')
            unlogged_params = ['self', 'x', 'y', 'callbacks', 'validation_data', 'verbose']
            return stop_log(self, original, args, kwargs, unlogged_params)

        settings = gorilla.Settings(allow_hit=True, store_hit=True)
        gorilla.apply(gorilla.Patch(tensorflow.keras.Model, 'fit', fit, settings=settings))
