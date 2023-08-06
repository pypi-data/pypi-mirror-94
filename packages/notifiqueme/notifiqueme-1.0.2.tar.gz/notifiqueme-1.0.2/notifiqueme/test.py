# -*- coding: utf-8 -*-
from notifiqueme import modulo
obj = modulo.Notification("72a98f45-d55b-426f-a9c2-802de831ad71", str("-bg+J-qumMtx+pU-KXt1PyFfNmRGPS1+-j51aRGQ"))
p = obj.Send(5531989715963, "11- credenciais da conta do michael", modulo.NotificationType.WHATSAPP)
print(p)