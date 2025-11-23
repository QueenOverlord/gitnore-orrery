import torch
import torch.nn as nn
import random

# --- PART 1: THE READER ---
class Encoder(nn.Module):
    def __init__(self, input_dim, emb_dim, hid_dim, n_layers, dropout):
        super().__init__()
        
        # The tools
        self.hid_dim = hid_dim
        self.n_layers = n_layers
        
        # Tool 1: Dictionary (ID -> Vector)
        self.embedding = nn.Embedding(input_dim, emb_dim)
        
        # Tool 2: The Brain (LSTM)
        self.lstm = nn.LSTM(emb_dim, hid_dim, n_layers, dropout=dropout, batch_first=True)
        
        # Tool 3: The Filter (Regularization)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, src):
        # src is the list of context tags [batch_size, src_len]
        
        # Step 1: Turn IDs into Vectors
        embedded = self.dropout(self.embedding(src))
        
        # Step 2: Process with LSTM
        # We ignore 'outputs' because we only care about the final summary
        outputs, (hidden, cell) = self.lstm(embedded)
        
        # Output: The final mental state (Context Vector)
        return hidden, cell


# --- PART 2: THE WRITER ---
class Decoder(nn.Module):
    def __init__(self, output_dim, emb_dim, hid_dim, n_layers, dropout):
        super().__init__()
        
        self.output_dim = output_dim
        self.hid_dim = hid_dim
        self.n_layers = n_layers
        
        self.embedding = nn.Embedding(output_dim, emb_dim)
        self.lstm = nn.LSTM(emb_dim, hid_dim, n_layers, dropout=dropout, batch_first=True)
        
        # Tool 3: The Classifier (Projects hidden state -> Vocabulary size)
        self.fc_out = nn.Linear(hid_dim, output_dim)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, input, hidden, cell):
        # input = The single rule we just wrote [batch_size]
        
        # Add a dimension because LSTM expects a sequence, even if it's length 1
        input = input.unsqueeze(1) 
        
        embedded = self.dropout(self.embedding(input))
        
        # Update mental state based on this new input
        output, (hidden, cell) = self.lstm(embedded, (hidden, cell))
        
        # Predict the probability of the next line
        prediction = self.fc_out(output.squeeze(1))
        
        return prediction, hidden, cell


# --- PART 3: THE MANAGER ---
class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder, device):
        super().__init__()
        
        self.encoder = encoder
        self.decoder = decoder
        self.device = device
        
        # Safety Check: Encoder and Decoder must have same brain size
        assert encoder.hid_dim == decoder.hid_dim, \
            "Hidden dimensions of encoder and decoder must match!"
            
    def forward(self, src, trg, teacher_forcing_ratio=0.5):
        # src = Context tags
        # trg = The actual correct .gitignore file (target)
        
        batch_size = trg.shape[0]
        trg_len = trg.shape[1]
        trg_vocab_size = self.decoder.output_dim
        
        # Create a placeholder to store our predictions
        outputs = torch.zeros(batch_size, trg_len, trg_vocab_size).to(self.device)
        
        # 1. ENCODE: Get the thought vector from the source
        hidden, cell = self.encoder(src)
        
        # 2. PRIMING: The first input is always the <sos> token
        input = trg[:, 0]
        
        # 3. LOOP: Generate line by line
        for t in range(1, trg_len):
            # Decode step
            output, hidden, cell = self.decoder(input, hidden, cell)
            
            # Store prediction
            outputs[:, t, :] = output
            
            # 4. TEACHER FORCING (The 'Training Wheels')
            # Randomly decide: Use what we just predicted? Or use the correct answer?
            # This helps the model learn faster early on.
            teacher_force = random.random() < teacher_forcing_ratio
            top1 = output.argmax(1) 
            
            # Set the input for the NEXT loop iteration
            input = trg[:, t] if teacher_force else top1
            
        return outputs