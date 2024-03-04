import cv2
from pyzbar.pyzbar import decode 
from datetime import datetime
import geocoder
import os

class QrKodKaydedici:

  def __init__(self, dosya_adi):
    self.dosya_adi = dosya_adi
    self.kaydedilmis_kodlar = set()

    # Dosya yoksa oluşturun.
    if not os.path.exists(self.dosya_adi):
      with open(self.dosya_adi, "w") as dosya:
        pass

  def qr_kod_kaydet(self, qr_kod_icerigi):
    """
    QR kodunu dosyaya kaydeder.

    Parametreler:
      qr_kod_icerigi: QR kodunun içeriği.
    """

    # QR kod daha önce kaydedildiyse geri dön.
    if qr_kod_icerigi in self.kaydedilmis_kodlar:
      return

    # QR kodunu kaydet.
    self.kaydedilmis_kodlar.add(qr_kod_icerigi)

    # QR kodunu dosyaya yaz.
    with open(self.dosya_adi, "a") as dosya:
      dosya.write(qr_kod_icerigi + "\n")

def qr_kod_oku(goruntu):
  """
  Görüntüden QR kodunu okur.

  Parametreler:
    goruntu: Görüntü.

  Döndürülen değerler:
    qr_kod_icerigi: QR kodunun içeriği.
  """
  list1 =[]
  # QR kodunu algılamak için ZBar'ı kullanın.
  qr_kodlar = decode(goruntu)

  # QR kod bulunamadıysa boş bir dize döndürün.
  if qr_kodlar:
      qr_kod_icerigi = qr_kodlar[0].data.decode("utf-8")
      # QR kodunun konumunu al
      x1, y1, w, h = qr_kodlar[0].rect
      x2, y2 = x1 + w, y1 + h
      list1.append(x1)
      list1.append(y1)
      list1.append(x2)
      list1.append(y2)
  else:
      qr_kod_icerigi = ""
  
  return list1, qr_kod_icerigi 


def goruntuyu_isleme(goruntu):
  """
  Görüntüyü işler ve QR kodunu okur.

  Parametreler:
    goruntu: Görüntü.

  Döndürülen değerler:
    qr_kod_icerigi: QR kodunun içeriği.
  """

  # Görüntüyü gri tonlamaya dönüştürün.
  gri_tonlama_goruntu = cv2.cvtColor(goruntu, cv2.COLOR_BGR2GRAY)

  # QR kodunu okuyun.
  list1,qr_kod_icerigi = qr_kod_oku(gri_tonlama_goruntu)

  # QR kod bulunamadıysa boş bir dize döndürün.
  if qr_kod_icerigi:
      # Zaman ve konum bilgilerini alın.
      zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      konum = geocoder.ip('me').city
      
      # QR kodunu işaretleyin.
      cv2.putText(goruntu, qr_kod_icerigi, (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
      cv2.putText(goruntu, zaman, (10, 440), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
      cv2.putText(goruntu, konum, (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
      cv2.rectangle(goruntu, (list1[0], list1[1]), (list1[2], list1[3]), (0, 255, 0), 2)

  return goruntu

def main():
  """
  Video dosyasını açar ve QR kodunu okur.
  """

  # Video dosyasını açın.
  video_yolu="Kayit_01.mp4"
  cap = cv2.VideoCapture(video_yolu)

  # QR kod kaydediciyi oluşturun.
  qr_kod_kaydedici = QrKodKaydedici("qr_kodlar.txt")
 

  # Sonsuz döngüye girin.
  while cap.isOpened():

    # Videodan bir kare okuyun.
    ret, goruntu = cap.read()

    # Görüntüyü işle.
    if ret:
        goruntu=goruntuyu_isleme(goruntu)
        cv2.imshow("QR Kod Okuyucu", goruntu)
    else:
        break

    # 'q' tuşuna basılırsa döngüden çıkın.
    if cv2.waitKey(1) & 0xFF == ord("q"):
      break

  # Video dosyasını kapatın.
  cap.release()
  print("QR code")
  # Tüm pencereleri kapatın.
  cv2.destroyAllWindows()

if __name__ == "__main__":
  main()
