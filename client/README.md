The dirs app/js and app/partials are protected by using http_secure_link module of nginx. In order to be able to request files in these dirs a client should have two valid cookies sl_hash and sl_expires_at:

sl_hash = md5($secret$http_user_agent$expires_at)

These cookies could be fetched by requesting http://app.anmec.me/account/auth/secure_link/. They are dropped on the course of authentication transition at app/authTransition.html.

If an user tries to request any partial from app/partial, the server should return the default partial for unauthenticated users: app/partials/unauthenticated.html
