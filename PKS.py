import sys

from toolbox.pairinggroup import  ZR,G1,G2,pair

from toolbox.hash_module import Hash, Exp


class PEKSClient:

   def __init__(self, grpObj):
      global group, h1
      group = grpObj
      group.H = self.H

      h1 = Hash('sha1', group)

   def H(self, args, type=G1):
      return group.hash(args, type)


   '''KeyGen(s): The security parameter s determines the size of the prime order p of the groups G_1and G_2. 
   The legal authority then also selects a random α∈Z_p^* and a generator g of G_1. 
   The Output is a public key A_pub=[g,h=g^α] and a private key α. The public key is then distributed to the messaging server.'''
   def KeyGen(self):
       #select a random group element
      g = group.random(G1)
       #get the private key alpha
      self.priv = group.random(ZR)
       #calculate public key
      self.pub = (g, g ** self.priv)
      print ('KeyGen(s): Public Key: %s' % g ** self.priv)
      print('KeyGen(s): Private Key: %s' % self.priv)
      return self.pub

   ''' PKS(A_pub,W): Using the public key and a word W, 
      the messaging server computes a bilinear map t =e(H_1 (W),h^r )∈G_2 using the random oracle and a random r∈Z_p^*. 
      Then outputs a searchable encryption PKS(A_pub,W)=[g^r,H_2 (t)]. '''
   def PEKS(self, word):
      g, h = self.pub
      r = group.random(ZR)
      print('PKS(A_pub,W): Public Key: %s' % h)
      t = pair(group.hash(word, G2), h ** r)
      print('PKS(A_pub,W): Pait t: %s' % t)
      return (g ** r, h1.hashToZn(t))

   '''	Trapdoor(A_priv,W): 
   The legal authority uses the random oracle and its private key to generate a trapdoor T_w=H_1 (W)^α∈G_1'''
   def Trapdoor(self, word):
      print('Trapdoor: %s for word: %s' % (group.hash(word, G1) ** self.priv, word))
      return group.hash(word, G1) ** self.priv


class PEKSServer:
   def __init__(self, grpObj, pub):
      global group, h2
      group = grpObj
      group.H = self.H
      h2 = Hash('sha1', group)
      self.pub = pub

   def H(self, args, type=G2):
      return group.hash(args, type)

   '''	Test(A_pub,S,T_W): When the messaging server receives a 
   Test function from the legal authority as S=[A,B] it can test if H_2 (e(T_w,A))=B'''
   def Test(self, s, tw):
      a, b = s
      print(h2.hashToZn(pair(tw, a)))
      print(b)
      return h2.hashToZn(pair(tw, a)) == b