
TOKEN_VIEW=eyToken
TOKEN_OWNER=eyToken

echo "Authorization: bearer $TOKEN_OWNER"

echo "GET"
curl -X GET -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/birds'
echo ""
echo ""
echo ""
echo "GET"
curl -X GET -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/birds/1'
echo ""
echo ""
echo ""
echo "POST"
curl -X POST -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" -d '{"common_name": "Test flamingo","habitats": [2, 3],"image_link":"example url","species": "Phoenicopterus ruber"}' 'https://birds-of-the-world-backend.onrender.com/birds'
echo ""
echo ""
echo ""
echo "PATCH"
curl -X PATCH -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" -d '{"common_name": "bird patched","habitats": [2, 3],"image_link":"example url","species": "Phoenicopterus ruber"}' 'https://birds-of-the-world-backend.onrender.com/birds/1'
echo ""
echo ""
echo ""
echo "DELETE"
curl -X DELETE -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/birds/1'
echo ""
echo ""
echo ""
echo "GET"
curl -X GET -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/habitats'
echo ""
echo ""
echo ""
echo "GET"
curl -X GET -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/habitats/1'
echo ""
echo ""
echo ""
echo "POST"
curl -X POST -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" -d '{"name": "Test Europe","region_id": 1}' 'https://birds-of-the-world-backend.onrender.com/habitats'
echo ""
echo ""
echo ""
echo "POST"
curl -X POST -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" -d '{"search": "Af"}' 'https://birds-of-the-world-backend.onrender.com/habitats'
echo ""
echo ""
echo ""
echo "PATCH"
curl -X PATCH -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" -d '{"name": "Patched habitat","region_id": 1}' 'https://birds-of-the-world-backend.onrender.com/habitats/1'
echo ""
echo ""
echo ""
echo "DELETE"
curl -X DELETE -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/habitats/1'
echo ""
echo ""
echo ""
echo "GET"
curl -X GET -H "Authorization: bearer $TOKEN_OWNER" -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/regions'
echo ""
echo ""
echo ""



