from core import env_loader

print(env_loader.get("APP_ENV"))
print(env_loader.get("WS_HOSTNAME"))
print(env_loader.get("WS_PORT"))


from core.services.spam_ham_scoring_ws.api_email_scoring import get_payload_spam_ham


response = get_payload_spam_ham("Nobody Beats Our Pricing And Quality. #1 Rated Backlink Building SEO Agency. Get Started.\
1,500+ SEO's Use Our Backlink Service Every Month To Power Their SEO Campaign.\
\
Our backlink service is used and trusted by 1,500+ digital marketing agencies to power their clients SEO. Whether you're a business owner or an agency, we can help propel your SEO.\
\
Check out for the Best SEO LINK BUILDING Packages: https://alwaysdigital.co/lgt/\
\
\
 kindra.hugo24@gmail.com")
if "ok" in response.get("status"):
    print(response.get("classification"))


response = get_payload_spam_ham("Hola Christian que tal,\
Mira te contacto para verificar contigo si ma;ana podriamos vernos sobre las 11.\
\
De hecho, por de momento sigo fuera de Madrid asi que no veo otra manera.\
\
Te agradezco de antemano. \
Benedicto V.")
if "ok" in response.get("status"):
    print(response.get("classification"))