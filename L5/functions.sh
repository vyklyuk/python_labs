function python-uni-auth {
  local JSON=$(\
    jq -jn \
    --arg username "${AUTH_USERNAME}" \
    --arg password "${AUTH_PASSWORD}" \
    '{"username":$username,"password":$password}' \
  )
  curl -s -XPOST "http://localhost:5000/api/v1/auth" \
    -H "Content-Type:application/json" \
    --data ${JSON} | jq -jr ".access_token"
}

function python-uni-create-user {
    local JSON=$(\
      jq -jn \
      --arg email "${EMAIL}" \
      --arg password "${PASSWORD}" \
      '{"email":$email,"password":$password,"first_name":"First", "last_name":"Last"}' \
    )
    curl -XPOST "http://localhost:5000/api/v1/user" \
      -H "Content-Type:application/json" \
      -H "Authorization: JWT $(python-uni-auth)" \
      --data "${JSON}"
}

function python-uni-create-wallet {
    local JSON=$(jq -jn --arg name "${WALLET_NAME}" '{"name": $name}')
    curl -XPOST "http://localhost:5000/api/v1/wallet" \
      -H "Content-Type:application/json" \
      -H "Authorization: JWT $(python-uni-auth)" \
      --data "${JSON}"
}

function python-uni-list-wallets {
    curl -XGET "http://localhost:5000/api/v1/wallet" \
      -H "Content-Type:application/json" \
      -H "Authorization: JWT $(python-uni-auth)" \
}

function python-uni-send-funds {
    local JSON=$(\
        jq -jn \
        --arg to_wallet "${TO_WALLET}" \
        --argjson amount "${AMOUNT}" \
        '{"to_wallet":$to_wallet,"amount":$amount}' \
    )
    curl -XPOST "http://localhost:5000/api/v1/wallet/${FROM_WALLET}/send-funds" \
        -H "Content-Type:application/json" \
        -H "Authorization: JWT $(python-uni-auth)" \
        --data "${JSON}"
}