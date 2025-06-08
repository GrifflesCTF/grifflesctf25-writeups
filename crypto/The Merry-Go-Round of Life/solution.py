def reverse_swap(scrambled, max_k=42):
    length = len(scrambled)
    for k in range(max_k, 0, -1): 
        swapped = [False] * length
        flag_list = list(scrambled)
        
        for n in range(length):
            if not swapped[n]:
                swap_pos = (n + k) % length
                if not swapped[swap_pos]:
                    flag_list[n], flag_list[swap_pos] = flag_list[swap_pos], flag_list[n]
                    swapped[n] = True
                    swapped[swap_pos] = True
        
        scrambled = ''.join(flag_list)    
    return scrambled

scrambled = "_A&im#lKQfL1r}ng4$wTrF02NxvG?B*T!~0@kh#4g1@${8Fg3PsY93JC3+5e_9736_RWfz%_"

flag = reverse_swap(scrambled)

print(flag)
