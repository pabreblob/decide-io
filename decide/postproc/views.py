from rest_framework.views import APIView
from rest_framework.response import Response
import random

class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)


    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'WEIGHTED':
            return self.weightedOptions(opts)
        elif t=='RANDOM':
            return self.randomSelection(opts)
        return Response({})
    #Each option has an assigned weight. The votes each option has received will be multiplied by their corresponding weight
    def weightedOptions(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes']*opt['weight'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    #Only one option is chosen and returned. Options are chosen randomly, taking into account the percentage of votes each option got.
    def randomSelection(self, options):
        out = []
        totalVotes=0
        for opt in options:
            totalVotes+=opt['votes']

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            })
        out.sort(key=lambda x: -x['postproc'])
        random.seed()
        randomNumber=random.randint(1,100)
        percentageAccumulated=0.0
        for o in out:
            if randomNumber-((o['votes']/totalVotes)*100+percentageAccumulated)<=0:
                chosen=o
                percentageAccumulated += (o['votes'] / totalVotes) * 100
                break
            percentageAccumulated+=(o['votes']/totalVotes)*100
        res=[]
        res.append({
                **chosen,
                'randomNumber': randomNumber,
                'percentageAccumulated':percentageAccumulated
            })
        return Response(res)