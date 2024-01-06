
TOKEN_VIEW=eyToken
TOKEN_OWNER=eyToken

echo "Authorization: bearer $TOKEN_OWNER"

echo "GET"
curl -X GET -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'http://127.0.0.1:5000/birds'
echo ""
echo ""
echo ""
echo "GET"
curl -X GET -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'http://127.0.0.1:5000/birds/1'
echo ""
echo ""
echo ""
echo "POST"
curl -X POST -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" -d '{"common_name": "Test flamingo","habitats": [2, 3],"image_link":"example url","species": "Phoenicopterus ruber"}' 'http://127.0.0.1:5000/birds'
echo ""
echo ""
echo ""
echo "PATCH"
curl -X PATCH -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" -d '{"common_name": "bird patched","habitats": [2, 3],"image_link":"example url","species": "Phoenicopterus ruber"}' 'http://127.0.0.1:5000/birds/1'
echo ""
echo ""
echo ""
echo "DELETE"
curl -X DELETE -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'http://127.0.0.1:5000/birds/1'
echo ""
echo ""
echo ""
echo "GET"
curl -X GET -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'http://127.0.0.1:5000/habitats'
echo ""
echo ""
echo ""
echo "GET"
curl -X GET -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'http://127.0.0.1:5000/habitats/1'
echo ""
echo ""
echo ""
echo "POST"
curl -X POST -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" -d '{"name": "Test Europe","region_id": 1}' 'http://127.0.0.1:5000/habitats'
echo ""
echo ""
echo ""
echo "POST"
curl -X POST -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" -d '{"search": "Af"}' 'http://127.0.0.1:5000/habitats'
echo ""
echo ""
echo ""
echo "PATCH"
curl -X PATCH -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" -d '{"name": "Patched habitat","region_id": 1}' 'http://127.0.0.1:5000/habitats/1'
echo ""
echo ""
echo ""
echo "DELETE"
curl -X DELETE -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'http://127.0.0.1:5000/habitats/1'
echo ""
echo ""
echo ""
echo "GET"
curl -X GET -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'http://127.0.0.1:5000/regions'
echo ""
echo ""
echo ""



