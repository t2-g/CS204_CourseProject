# Example data memory and instruction memory implemented as dictionaries
data_memory = {0: 0, 4: 0, 8: 0, 12: 0}
instruction_memory = {0: b'\x00\x00\x00\x00', 4: b'\x00\x00\x00\x00', 8: b'\x00\x00\x00\x00', 12: b'\x00\x00\x00\x00'}

class Cache:
    def __init__(self, size, block_size, associativity, replacement_policy,ways):
            self.size = size
            self.block_size = block_size
            self.associativity = associativity
            self.replacement_policy = replacement_policy
            self.number_of_index_bits = self.ways = ways
            self.number_of_block_offset_bits = int(math.ceil(math.log(block_size, 2)))
            self.num_blocks = size // block_size
            self.num_sets = self.num_blocks // associativity
            self.data = [[0] * block_size for i in range(self.num_blocks)]
            # For Reads
            self.count_reads = 0
            self.count_read_hits = 0
            self.count_read_misses = 0
            # For writes
            self.count_writes = 0
            self.count_write_hits = 0
            self.count_write_misses = 0
        
    def tag_array_defn(self,address):
            address = hex(address)
            address = bin(int(address[2:], 16))[2:]
            address = (32 - len(address)) * '0' + address
            return address
    
    def get_param(self,tag_array):
            tag = int(tag_array[:-(self.number_of_block_offset_bits+self.number_of_index_bits)], 2)
            self.number
            if self.number_of_index_bits ==0:
                index=0;
            else:
                index=int(address[-(self.number_of_block_offset_bits+self.number_of_index_bits):-self.number_of_block_offset_bits], 2)    
    
    def set(self):
            if self.associativity ==0:
                self.sets =1
                self.ways =self.size//self.block_size
            elif self.associativity==1:
                self.sets = self.cache_size // self.block_size
                self.number_of_index_bits = int(math.ceil(math.log(self.sets, 2)))
                self.ways = 1
            else:
                self.sets = self.cache_size // self.block_size
                self.sets = self.sets // self.ways
                self.number_of_index_bits = int(math.ceil(math.log(self.sets, 2)))

            self.cache = [dict() for i in range(self.sets)] # {tag: (block, recency)}
        
             
            
    def read(self, address):
        set_index = self.get_set_index(address)
        tag = self.get_tag(address)
        for i in range(set_index * self.associativity, (set_index + 1) * self.associativity):
            if self.tag[i] == tag:
                self.access_counter[i] += 1
                return self.data[i][address % self.block_size]
        # Cache miss
        block_index = self.replacement_policy(
            self.access_counter[set_index * self.associativity:(set_index + 1) * self.associativity])
        self.tag[block_index] = tag
        self.access_counter[block_index] = max(self.access_counter) + 1
        # Fetch data from memory
        data = fetch_data_from_memory(address)
        self.data[block_index] = data
        return data[address % self.block_size]

    def write(self, address, data):
        set_index = self.get_set_index(address)
        tag = self.get_tag(address)
        for i in range(set_index * self.associativity, (set_index + 1) * self.associativity):
            if self.tag[i] == tag:
                self.access_counter[i] += 1
                self.data[i][address % self.block_size] = data
                return
        # Cache miss
        block_index = self.replacement_policy(
            self.access_counter[set_index * self.associativity:(set_index + 1) * self.associativity])
        self.tag[block_index] = tag
        self.access_counter[block_index] = max(self.access_counter) + 1
        # Write data to cache
        self.data[block_index][address % self.block_size] = data
        # Write data to memory
        write_data_to_memory(address, data)
