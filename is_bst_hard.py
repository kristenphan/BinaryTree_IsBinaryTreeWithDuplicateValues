#!/usr/bin/python3

import sys, threading
import collections

sys.setrecursionlimit(10**8) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

# this class represents a node in a binary tree
class Node:
    def __init__(self, key, left=None, right=None, m=float("-inf"), M=float("inf")):
        self.key = key
        self.left = left
        self.right = right
        self.m = m # min value of all of the node's left descendants
        self.M = M # max value of all of the node's right descendants


# this function reads the input
# builds and returns: (1) n - number of nodes in the tree (2) the root the of the tree
def read():
    n = int(sys.stdin.readline())
    #n = int(file.readline().strip())
    key = [0 for i in range(n)]
    left = [0 for i in range(n)]
    right = [0 for i in range(n)]
    for i in range(n):
        [a, b, c] = map(int, sys.stdin.readline().split())
        #[a, b, c] = map(int, file.readline().split())
        key[i] = a
        left[i] = b
        right[i] = c

    assert (n == len(key) and len(key) == len(left) and len(left) == len(right))

    tree = [Node(key[i], left[i], right[i]) for i in range(n)]

    # build a binary tree from input
    for i in range(n):
        if tree[i].left != -1:
            temp = tree[i].left
            tree[i].left = tree[temp]
        if tree[i].right != -1:
            temp = tree[i].right
            tree[i].right = tree[temp]

    # if the tree is empty or has only one node, return n and None for the root as the root of the tree does not matter in this scenario
    if n == 0 or n == 1:
        return n, None

    return n, tree[0] # return n and the root of the binary tree

# this function traverses through a binary tree rooted at the passed in node in a post-order fashion
# and returns a list of nodes arranged in the same order as the post-order traversal path
def postOrder(node, post_order_nodes):
    # if the node is a leaf,
    # append the node to post_order_nodes to document the traversal path and then return to the key's parent
    if node.left == -1 and node.right == -1:
        post_order_nodes.append(node)
        return

    # if the node has a left child, traverse down that path
    if node.left != -1:
        postOrder(node.left, post_order_nodes)

    # if the node has a right child, traverse down that path
    if node.right != -1:
        postOrder(node.right, post_order_nodes)

    # append the node to post_order_nodes after done traversing through its left descendants and right descendants
    # to document the traversal path
    post_order_nodes.append(node)


# this function takes in the root of a binary tree
# and check if the tree is a BST in accordance with the definition stated in main()
# if yes, return True
# if no, return False
# this algorithm traverses the tree from bottom up by following its post-order traversal path
# checks if each node is a valid node (ie. the condition of a BST is met at that node) and updates the nodes accordingly
def IsBinarySearchTree(root):
    post_order_nodes = []
    postOrder(root, post_order_nodes)
    # traverse the nodes from bottom up, same order as the post-order path
    for node in post_order_nodes:
        # for leaf nodes:
        # update the min and max values to be equal to the node's key
        # then proceed to the next node
        # no need to validate this node as a leaf node by itself is already a BST
        if node.left == -1 and node.right == -1:
            node.m = node.key
            node.M = node.key
            continue

        # for non-leaf nodes:
        # validate the node by checking if the condition of a BST is being upheld at this node
        # a node is considered valid in a BST if it satisfies a two-part condition:
        # (1) the Max value of all of the node's left descendants is strictly smaller than the node's key
        # (2) the min value of all of the node's right descendants are greater than or equal to the node's key
        if node.left != -1:
            if node.key <= node.left.M:
                return False
        if node.right != -1:
            if node.key > node.right.m:
                return False

        # once the node is confirmed as valid, update the node's min and max value
        # set the node's min value to its left child's min value
        # if the node does not have a left child, set its min value to its key
        if node.left != -1:
            node.m = node.left.m
        else:
            node.m = node.key
        # set the node's Max value to its right child's Max value
        # if the node does not have a right child, set its Min value to its key
        if node.right != -1:
            node.M = node.right.M
        else:
            node.M = node.key

    return True


# this program reads the input, a valid binary tree,
# check if the tree is a BST in accordance with the below definition
# if yes, output 'CORRECT'. otherwise, output 'INCORRECT'
# definition of a BST tree with possibly duplicate keys:
# --- for any node of the tree, if its key is 𝑥, then for any node in its left subtree,
# --- its key must be strictly less than 𝑥,
# --- and for any node in its right subtree,
# --- its key must be greater than or equal to 𝑥.
# --- In other words, smaller elements are to the left, bigger elements are to the right,
# --- and duplicates are always to the right.
# the program uses IsBinarySearchTree() to determine if a tree is a BST. See comments in IsBinarySearchTree() to see how this algorithm works
# EXAMPLE 1:
# input:
# 7
# 5 1 2
# 3 3 4
# 8 5 6
# 1 -1 -1
# 4 -1 -1
# 2 -1 -1
# 9 -1 -1
# output: INCORRECT
# tree built from the input is visualized as below
#                 5 < ----------------root. condition of a BST is violated here
#              /      \
#            3         8
#          /  \      /  \
#        1     4   2     9
# EXAMPLE 2:
# input:
# 8
# 5 1 2
# 3 3 4
# 8 5 6
# 1 -1 -1
# 4 -1 7
# 5 -1 -1
# 9 -1 -1
# 5 -1 -1
# output: INCORRECT
# tree built from the input is visualized as below
#               5 <--------------------------- root
#             /   \
#           3       8 <----------------------- condition of a BST violated at this node
#         /  \     /
#       2     3   8  <------------------------ condition of a BST violated at this node
#                /
#               8
# even though the in-order traversal path of this tree is not a sorted list ([2, 3, 3, 5, 6, 8, 8]),
# the tree failed test #2 and is not a BST
# EXAMPLE 3:
# input:
# 3
# 5  -1  1
# 5  -1  2
# 10 -1 -1
# output: CORRECT
# tree built from input is visualized as below:
#    5 <-------------- root
#     \
#      5
#       \
#       10
# because the in-order traversal path is a sorted list ([5, 5, 10])
# and all nodes in the tree meet the condition of a BST, the tree is a BST
# EXAMPLE 4:
# input:
# 5
# 10  1  2
# 5  -1 -1
# 15  3  4
# 10 -1 -1
# 20 -1 -1
# output: CORRECT
# tree built from input is visualized as below:
#        10 <----------------- root
#       /   \
#      5     15
#           /  \
#         10    20
# because its in-order traversal path is a sorted list ([5, 10, 10, 15, 20])
# and the biggest node of the root's left child branch is smaller than the root,
# the tree is a BST
# EXAMPLE 5:
# input:
# 4
# 10 -1 1
# 20 2 -1
# 15 -1 3
# 20 -1 -1
# output: INCORRECT
# tree built from input is visualized as below
#       10 <--------------- root
#        \
#         20 <----------------- condition of a BST is violated at this node
#        /
#       15
#         \
#          20
# EXAMPLE 6:
# input:
# 12
# 20 1 2
# 7 3 4
# 20 -1 -1
# 5 5 6
# 10 7 8
# 2 -1 -1
# 6 -1 -1
# 8 9 10
# 20 11 -1
# 7 -1 -1
# 9 -1 -1
# 15 -1 -1
# output: INCORRECT
# tree is built and visualized as below
#                  20 <----------------- root. condition of a BST is violated at this node
#               /      \
#             7         20
#          /     \
#         5        10
#       /  \     /   \
#      2    6   8     20
#              / \    /
#             7   9  15
def main():
    n, root = read()
    # if a tree is emtpy or has only one node, it's a BST
    if n == 0 or n == 1:
        print ('CORRECT')
    # otherwise, traverse through the tree and check if it's a BST in accordance with the definition above
    else:
        if IsBinarySearchTree(root):
            print("CORRECT")
        else:
            print("INCORRECT")


threading.Thread(target=main).start()
