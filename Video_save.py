import cv2

def video_kaydet(video_adi, sure_saniye):
    # Video çözünürlüğünü ve frame hızını ayarlayın
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = 20  # Örnek frame hızı (fps)

    # VideoWriter objesi oluşturun
    out = cv2.VideoWriter(video_adi, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (frame_width, frame_height))

    # Belirli bir süre boyunca videoyu kaydet
    baslangic_zamani = cv2.getTickCount()
    while True:
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('Video Kaydediliyor...', frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')) or ((cv2.getTickCount() - baslangic_zamani) / cv2.getTickFrequency() > sure_saniye):
            break

    # VideoWriter ve VideoCapture nesnelerini serbest bırakın
    cap.release()
    out.release()
    cv2.destroyAllWindows()



def video_izle(video_yolu):
    cap = cv2.VideoCapture(video_yolu)

    # Video dosyasının başarıyla açılıp açılmadığını kontrol edin
    if not cap.isOpened():
        print("Video dosyası açılamadı!")
        return

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            # Frame'i göster
            cv2.imshow('Video', frame)

            # 'q' tuşuna basarak videoyu kapat
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    # Videoyu serbest bırak ve pencereyi kapat
    cap.release()
    cv2.destroyAllWindows()



# Belirli bir süre (örneğin 20 saniye) boyunca video kaydedin, .mp4 uzantısıyla
video_kaydet('kayit_02.mp4', sure_saniye=10)


#İzlemek istediğiniz video dosyasının yolunu belirtin
video_yolu = 'kayit_02.mp4'

# Videoyu izleyin
video_izle(video_yolu)
