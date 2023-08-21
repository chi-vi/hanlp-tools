#! python
# -*- mode: python ; coding: utf-8 -*-

import os, re, requests, getpass

URL = "https://chivi.app/_wn"
CLIENT = requests.Session()

os.environ["HANLP_HOME"] = ".hanlp"
# os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"
# os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"

import hanlp, torch

MTL_TASK = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)

def get_max_ch_no(wn_id, sname):
  url = f"{URL}/seeds/{wn_id}/{sname}/brief"
  res = CLIENT.get(url)

  return res.json()["chap_count"]

def read_txt_file(path):
  with open(path, 'r', encoding="utf-8") as file:
    return file.read()

def write_mtl_file(mtl_path, mtl_data):
  with open(mtl_path, 'w', encoding="utf-8") as mtl_file:
    mtl_file.write(mtl_data.to_json())

def write_con_file(con_path, con_data):
  with open(con_path, 'w', encoding="utf-8") as con_file:
    line_idx = 0

    for con_line in con_data:
        con_file.write(re.sub('\\n(\\s+)', ' ', str(con_line)))
        con_file.write('\n')
        line_idx += 1

def split_array(list, size):
  output = []

  for i in range(0, len(list), size):
    output.append(list[i:i+ size])

  return output

def analyze_chap(wn_id, ch_no, cksum, parts):
  for p_idx, inp_data in enumerate(parts):
    inp_text = inp_data.split('\n')

    con_path = f"output/{wn_id}/{ch_no}-{cksum}-{p_idx}.con"
    mtl_path = f"output/{wn_id}/{ch_no}-{cksum}-{p_idx}.mtl"

    if os.path.isfile(con_path) and os.path.isfile(mtl_path):
      if p_idx > 0:
        print(f"  - Phần {p_idx} đã được phân tích, đang tải lên...")
    else:
      mtl_data = MTL_TASK(inp_text)

      write_con_file(con_path, mtl_data["con"])
      write_mtl_file(mtl_path, mtl_data)

      if p_idx > 0:
        print(f"  - Đã phân tích xong phần {p_idx}, đang tải lên...")

    json = {
      'wn_id': wn_id,
      'ch_no': ch_no,
      'cksum': cksum,
      'p_idx': p_idx,
      '_algo': 'electra_base',
      'con_text': read_txt_file(con_path),
      'mtl_json': read_txt_file(mtl_path),
    }

    url = "https://chivi.app/_wn/anlzs/chaps"
    res = CLIENT.post(url, json=json)

    if res.status_code < 300:
      if p_idx > 0:
        print(f"    Đăng tải thành công chương {ch_no} phần {p_idx}.")
        print(f"    Server trả về: {res.text}")
    else:
      print("    Đăng tải thất bại, mời thử lại sau!")
      print(res.text)


def run(wn_id, sname, chmin = 1, chmax = 0):
  out_dir = f"output/{wn_id}"
  os.makedirs(out_dir, exist_ok=True)

  for ch_no in range(chmin, chmax + 1):
    print(f"- Tải xuống text gốc chương [{ch_no}] nguồn [{sname}] truyện [{wn_id}]:")

    url = f"{URL}/texts/{wn_id}/{sname}/{ch_no}/parts"
    res = CLIENT.get(url).json()

    cksum = res["cksum"]
    parts = res["parts"]

    if cksum == "":
      print("  Chương tiết chưa có text gốc, mời kiểm tra lại!")
    else:
      print(f"  Đã lấy xuống text gốc, chương chia {len(parts) - 1} phần, checksum: [{cksum}].")
      print()
      analyze_chap(wn_id, ch_no, cksum, parts)

def do_login():
  email = os.environ.get("EMAIL", None)
  upass = os.environ.get("UPASS", None)

  print("\nThông tin đăng nhập Chivi:")

  if email is None:
    print("Hòm thư:", end=' ')
    email = input().strip()
  else:
    print(f"Hòm thư: {email}")

  if upass is None:
    upass = getpass.getpass("Mật khẩu: ").strip()

  json = {'email': email, 'upass': upass}
  res = CLIENT.post("https://chivi.app/_db/_user/log-in", json=json)

  if res.status_code < 300:
    user = res.json()["uname"]
    print(f"Xin chào {user}!")
    print()
  else:
    print("Đăng nhập thất bại, mời thử lại!")
    os.environ["EMAIL"] = None
    os.environ["UPASS"] = None

    do_login()

def read_str(prompt):
  while True:
    print(prompt, end=' ')
    value = input().strip()

    if value != "":
      return value

if __name__ == '__main__':
  do_login()

  wn_id = os.environ.get("WN_ID", None)
  if wn_id is None:
    wn_id = int(read_str("Nhập ID bộ truyện:"))
  else:
    print(f"ID bộ truyện: {wn_id}")
    wn_id = int(wn_id)

  sname = os.environ.get("SNAME", None)
  if sname is None:
    sname = read_str("Nhập nguồn chương:")
  else:
    print(f"Nguồn chương: {sname}")

  print("...Kiểm tra dữ liệu...", end=' ')

  url = f"{URL}/seeds/{wn_id}/{sname}/brief"
  res = requests.get(url).json()

  total = res["chap_count"]
  print(f"hoàn thành, nguồn truyện có tổng cộng {total} chương")

  chmin = 1
  chmax = 0

  chmin = os.environ.get("FROM", None)
  if chmin is None:
    print("Bắt đầu từ chương (mặc định là 1): ", end=' ')

    value = input().strip()
    if value == "":
      chmin = 1
    else:
      chmin = int(value)

  else:
    print(f"Chương bắt đầu: {chmin}")
    chmin = int(chmin)

  if chmin < 1:
    chmin = 1

  chmax = os.environ.get("UPTO", None)

  if chmax is None:
    print(f"Tới chương (mặc định là {total}): ", end=' ')
    value = input().strip()

    if value == "":
      chmax = 0
    else:
      chmax = int(value)
  else:
    print(f"Chương kết thúc: {chmax}")
    chmax = int(chmax)

  if chmax < chmin:
    chmax = total

  print(f"Bạn sẽ chạy chương trình phân tích dữ liệu các chương từ {chmin} tới {chmax} của bộ truyện {wn_id}")
  print(f"Lưu ý: Các chương đã được phân tích sẽ không phân tích lại, hãy kiểm tra trong thư mục output/{wn_id} nếu muốn dọn sạch rác!")

  run(wn_id, sname, chmin, chmax)
