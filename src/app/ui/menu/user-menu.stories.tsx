import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';

import UserMenu from './user-menu';


const meta = {
    title: 'Menu/UserMenu',
    component: UserMenu,
    tags: ['autodocs'],
} satisfies Meta<typeof UserMenu>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {};
