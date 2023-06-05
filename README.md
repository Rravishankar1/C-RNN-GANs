# Implementation of C-RNN-GAN.

Publication:
Title: C-RNN-GAN: Continuous recurrent neural networks with adversarial training
Information: http://mogren.one/publications/2016/c-rnn-gan/

Bibtex:

@inproceedings{mogren2016crnngan, 
  title={C-RNN-GAN: A continuous recurrent neural network with adversarial training}, 
  author={Olof Mogren}, 
  booktitle={Constructive Machine Learning Workshop (CML) at NIPS 2016}, 
  pages={1}, 
  year={2016}
}

## Requirements

tensorflow

## How to run?

python rnn_gan_tf2.py --datadir "./data/spy" --traindir "./outputs/spyout" --feed_previous --feature_matching --bidirectional_d --learning_rate 0.1 --pretraining_epochs 6

