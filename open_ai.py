
import openai




def DaVincibot(text):

    config = {
        "access_token": "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"
        }
    
    openai.api_key = "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"

    response = openai.Completion.create( engine="text-davinci-002", 
    prompt=text,
    max_tokens=1024)

    # print(response.get("choices"))

    vinReply = ""

    for i in range(len(response.get("choices"))):
        
        jsonArray = response.get("choices")[i]
        
        d =dict(jsonArray)
        
        vinReply = d.get("text")

    
    print(vinReply)
    return vinReply
    
        
    



# DaVincibot("what is cybersecurity")