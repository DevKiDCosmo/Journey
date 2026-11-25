#include <stdio.h>
#include <memory>

struct LinkedList {
    int *addr;
    LinkedList *next;
};

class RingBufferRegistration {
public:
    RingBufferRegistration() : m_data_addr(nullptr) {}
    static void Register(LinkedList* data);
    ~RingBufferRegistration();
private:
    LinkedList* m_data_addr;
};

void RingBufferRegistration::Register(LinkedList* data) {
    // Implementation for registering the data
    std::unique_ptr<LinkedList> ptr(data);
}

RingBufferRegistration::~RingBufferRegistration() {
    // Clean up registered nodes if necessary
    delete m_data_addr;
}

class RingBuffer {
public:
    // Default Constructor
    RingBuffer() : m_size(0), m_data(nullptr), m_head(0), m_tail(0), m_count(0) {}

    // Init RingBuffer with a specific size
    explicit RingBuffer(int size)
        : m_size(size), m_data(new int[size]), m_head(0), m_tail(0), m_count(0) {
        
        // Allocate and prepare linked list node for registration
        LinkedList* node = new LinkedList{m_data, nullptr};
        RingBufferRegistration::Register(node);
    }

    ~RingBuffer() {
        delete[] m_data;
    }

    // Core Ring Buffer Operations
    bool isFull() const {
        return m_count == m_size;
    }

    bool isEmpty() const {
        return m_count == 0;
    }

    bool push(int value) {
        if (isFull()) {
            return false; // Buffer is full
        }
        m_data[m_tail] = value;
        m_tail = (m_tail + 1) % m_size;
        m_count++;
        return true;
    }

    bool pop(int* value) {
        if (isEmpty()) {
            return false; // Buffer is empty
        }
        *value = m_data[m_head];
        m_head = (m_head + 1) % m_size;
        m_count--;
        return true;
    }

    int size() const {
        return m_count;
    }

    int capacity() const {
        return m_size;
    }

private:
    int m_size;
    int* m_data;
    int m_head;
    int m_tail;
    int m_count;
};

int main() {
    // Example usage:
    RingBuffer rb(5);

    rb.push(10);
    rb.push(20);
    rb.push(30);

    int val = 0;
    if (rb.pop(&val)) {
        printf("Popped: %d\n", val); // Output: Popped: 10
    }

    return 0;
}