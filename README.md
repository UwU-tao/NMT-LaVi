# Mô hình dịch máy Lào - Việt
Ứng dụng dự án MultilingualMT-UET-KC4.0 vào bài toán dịch máy Lào-Việt trong chủ đề bài tập lớn lớp Xử lý ngôn ngữ tự nhiên INT3406E 20.

## Nội dung

- [Cài đặt môi trường, thư viện](#cài-đặt-môi-trường-thư-viện)
- [Chuẩn bị dữ liệu](#bước-1-chuẩn-bị-dữ-liệu)
- [Huấn luyện mô hình](#bước-2-huấn-luyện-mô-hình)
- [Dịch](#bước-3-dịch)
- [Đánh giá chất lượng dựa trên điểm BLEU](#bước-4-đánh-giá-chất-lượng-dựa-trên-điểm-bleu)
- [Thành viên trong nhóm](#thành-viên-trong-nhóm)

## Cài đặt môi trường, thư viện

**Note**:
Lưu ý:
Phiên bản hiện tại chỉ tương thích với python>=3.6
```
git clone https://github.com/UwU-tao/NMT-LaVi.git
cd NMT-LaVi
pip install -r requirements.txt
```

## Bước 1: Chuẩn bị dữ liệu

Ví dụ thực nghiệm dựa trên cặp dữ liệu Lào - Việt với 80k cặp câu.

```bash
cd data/pre_processed
```

Dữ liệu bao gồm câu nguồn (`src`) và câu đích (`tgt`) dữ liệu đã được tách từ:

* `train2023.lo`
* `train2023.vi`
* `dev2023.lo`
* `dev2023.vi`
* `test.lo`
* `test.vi`

| Data set    | Sentences  |  Download  |
| :---------: | :--------: | :--------: |
| Training    | 75,872     | via GitHub |
| Development | 1,822      | via GitHub |
| Test        | 1,000      | via GitHub |


**Note**:
Lưu ý:
- Dữ liệu trước khi đưa vào huấn luyện cần phải được tokenize. 
- $CONFIG là đường dẫn tới vị trí chứa file config

Tách dữ liệu dev để tính toán hội tụ trong quá trình huấn luyện, thường không lớn hơn 5k câu.


## Bước 2: Huấn luyện mô hình

Để huấn luyện một mô hình mới **hãy chỉnh sửa file YAML config**:
Cần phải sửa lại file config en_vi.yml chỉnh siêu tham số và đường dẫn tới dữ liệu huấn luyện:

```yaml
# data location and config section
data:
  train_data_location: data/pre_processed/train2023
  eval_data_location:  data/pre_processed/dev2023
  src_lang: .lo 
  trg_lang: .vi 
log_file_models: 'model.log'
lowercase: false
build_vocab_kwargs: # additional arguments for build_vocab. See torchtext.vocab.Vocab for mode details
#  max_size: 50000
  min_freq: 5
# model parameters section
device: cuda
d_model: 512
n_layers: 6
heads: 8
# inference section
eval_batch_size: 8
decode_strategy: BeamSearch
decode_strategy_kwargs:
  beam_size: 5 # beam search size
  length_normalize: 0.6 # recalculate beam position by length. Currently only work in default BeamSearch
  replace_unk: # tuple of layer/head attention to replace unknown words
    - 0 # layer
    - 0 # head
input_max_length: 400 # input longer than this value will be trimmed in inference. Note that this values are to be used during cached PE, hence, validation set with more than this much tokens will call a warning for the trimming.
max_length: 160 # only perform up to this much timestep during inference
train_max_length: 150 # training samples with this much length in src/trg will be discarded
# optimizer and learning arguments section
lr: 0.2
optimizer: AdaBelief
optimizer_params:
  betas:
    - 0.9 # beta1
    - 0.98 # beta2
  eps: !!float 1e-9
n_warmup_steps: 4000
label_smoothing: 0.1
dropout: 0.1
# training config, evaluation, save & load section
batch_size: 64
epochs: 20
printevery: 200
save_checkpoint_epochs: 1
maximum_saved_model_eval: 5
maximum_saved_model_train: 5

```

Sau đó có thể chạy với câu lệnh:

```bash
python -m bin.main train --model Transformer --model_dir $MODEL/en-vi.model --config $CONFIG/en_vi.yml
```

**Note**:
Ở đây:
- $MODEL là dường dẫn tới vị trí lưu mô hình. Sau khi huấn luyện mô hình, thư mục chứa mô hình bao gồm mô hình huyến luyện, file config, file log, vocab.
- $CONFIG là đường dẫn tới vị trí chứa file config

## Bước 3: Dịch 

Mô hình dịch dựa trên thuật toán beam search và lưu bản dịch tại `$your_data_path/translate.la2vi.vi`.

```bash
python -m bin.main infer --model Transformer --model_dir $MODEL/la_vi.model --features_file $your_data_path/test.lo --predictions_file $your_data_path/translate.la2vi.vi
```

## Bước 4: Đánh giá chất lượng dựa trên điểm BLEU

Đánh giá điểm BLEU dựa trên multi-bleu

```bash
perl thrid-party/multi-bleu.perl $your_data_path/translate.la2vi.vi < $your_data_path/test.vi
```

|        MODEL       | BLEU (Beam Search) |
| :-----------------:| :----------------: |
| Transformer (Base) |        19.72       |

## Thành viên trong nhóm
Ngô Thượng Hiếu - 21021491\
Ngô Vịt Huy - 21020046\
Đồng Văn Dương - 21021470 

## Chi tiết tham khảo tại 
[nmtuet.ddns.net](http://nmtuet.ddns.net:1190/)

## Nếu có ý kiến đóng góp, xin hãy gửi thư tới địa chỉ mail kcdichdangu@gmail.com

## Xin trích dẫn bài báo sau:
```bash
@inproceedings{ViNMT2022,
  title = {ViNMT: Neural Machine Translation Toolkit},
  author = {Nguyen Hoang Quan, Nguyen Thanh Dat, Nguyen Hoang Minh Cong, Nguyen Van Vinh, Ngo Thi Vinh, Nguyen Phuong Thai, Tran Hong Viet},
  booktitle = {https://arxiv.org/abs/2112.15272},
  year = {2022},
}
```
