from typing import List


class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        return_list =[0]*(len(nums))
        nums_end=len(nums)-1
        nums_start=0
        list_pos=len(nums)-1
        while nums_start<=nums_end:
            nums_start_square=nums[nums_start]*nums[nums_start]
            nums_end_square=nums[nums_end]*nums[nums_end]
            if nums_start_square<=nums_end_square:
                return_list[list_pos]=nums_end_square
                nums_end-=1
            else :
                return_list[list_pos]=nums_start_square
                nums_start+=1
            list_pos-=1
        return return_list



if __name__ == '__main__':
    solo = Solution()
    print(solo.sortedSquares([-4,-1]))