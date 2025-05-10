import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from function.ReadSave import *

class My_Absa(Cleaning):
    def __init__(self,next_col='review'):
        super().__init__()
        self.next_col = next_col

    def next_clean(self,data):
        data[self.next_col] = data[self.next_col].apply(self.first_clean)
        return data

    def concat_clean(self, prep_file,gt_file ):
        prep = self.read_prep(prep_file)
        gt = self.read_gt(gt_file)
        gt.columns = ['name','score','review','time']
        gt = gt['review']
        gt.name='review'
        data = pd.concat([prep,gt],ignore_index=True, axis=1)
        data.columns=['nama','skor','ulasan','waktu','review']
        data = self.next_clean(data)
        return data.dropna(subset='review')

    def process_absa(self,prep_file,gt_file, save_file_name):
        from pyabsa import AspectTermExtraction as ATEPC, available_checkpoints
        checkpoint_map = available_checkpoints()
        aspect_extractor = ATEPC.AspectExtractor('English',
                                            auto_device=False,  # False means load model on CPU
                                            cal_perplexity=True,)    
        # instance inference
        data_init = self.concat_clean(prep_file, gt_file)
        
        inference_source = data_init['review'].astype(str).tolist()
        atepc_result = aspect_extractor.batch_predict(target_file=inference_source,  #
                                                save_result=True,
                      pred_sentiment=True,)
        data_absa = pd.DataFrame(atepc_result) 
        data_absa = data_absa[['aspect','sentiment']]                                         # Predict the sentiment of extracted aspect terms  
        data=pd.concat([data_init,data_absa], axis=1)
        self.save_pyabsa(data,save_file_name)
        return data
